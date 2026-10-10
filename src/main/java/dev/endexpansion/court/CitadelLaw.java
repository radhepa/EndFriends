package dev.endexpansion.court;

import dev.endexpansion.EndExpansion;
import dev.endexpansion.EndItems;
import dev.endexpansion.entity.Endarch;
import dev.endexpansion.entity.Settler;
import dev.endexpansion.talk.DialogueBank;
import dev.endexpansion.world.ResidentPiece;
import dev.endexpansion.world.Settlement;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import org.jspecify.annotations.Nullable;

/**
 * Guest-law. A player who crosses into a Citadel without Enderman Eyes is an outlaw there: the
 * Herald cries out and the whole Court attacks. With the Eyes they are a guest, but if the Eyes leave
 * their inventory while inside, or they strike any member of the Court, guest-law ends. Outlawry
 * lasts until they leave (it isn't remembered; Favor is, see {@link CourtFavor}).
 *
 * <p>Court mobs from spawn eggs belong to no Citadel: they attack players without the Eyes who come
 * within {@link #WILD_RANGE} blocks, and anyone who strikes them.
 */
public final class CitadelLaw {
    /** How close a Court mob with no Citadel lets a player without the Eyes come. */
    public static final double WILD_RANGE = 16.0;
    /** How far past a Citadel's walls an outlaw must go to be let be. */
    private static final int PARDON_MARGIN = 24;

    private static final Map<String, Set<UUID>> OUTLAWS = new ConcurrentHashMap<>();
    /** Which Citadel each player was last inside, and its bounds. */
    private static final Map<UUID, Visit> INSIDE = new HashMap<>();

    private record Visit(Settlement citadel, BoundingBox box) {}

    private CitadelLaw() {}

    public static boolean carriesEyes(Player player) {
        return player.getInventory().contains(stack -> stack.is(EndItems.ENDERMAN_EYES));
    }

    /** Whether this Court member should attack this target. */
    public static boolean isOutlaw(LivingEntity target, Settler member) {
        if (!(target instanceof ServerPlayer player) || player.isCreative() || player.isSpectator()) return false;
        Settlement citadel = member.settlement();
        if (OUTLAWS.getOrDefault(citadel.key(), Set.of()).contains(player.getUUID())) return true;
        return citadel.isWild() && member instanceof Mob mob && !carriesEyes(player) && player.distanceToSqr(mob) < WILD_RANGE * WILD_RANGE;
    }

    /** Whether the player may speak with the Court here: a guest bearing the Eyes, not an outlaw. */
    public static boolean isGuest(ServerPlayer player, Settler member) {
        return carriesEyes(player) && !OUTLAWS.getOrDefault(member.settlement().key(), Set.of()).contains(player.getUUID());
    }

    /** The player struck a member of the Court: guest-law ends, and the Court remembers. */
    public static void strike(ServerPlayer player, Settler member) {
        if (player.isCreative() || player.isSpectator()) return;
        Settlement citadel = member.settlement();
        boolean was = OUTLAWS.getOrDefault(citadel.key(), Set.of()).contains(player.getUUID());
        if (was) return;
        var favor = CourtFavor.get(player.level().getServer()).bond(citadel.key(), player.getUUID());
        favor.points = Math.max(0, favor.points - 20);
        outlaw(player, citadel, member instanceof Endarch e ? e : null, "broken_law");
    }

    /** Pardons a player at a Citadel (for tests and commands). */
    public static void pardon(ServerPlayer player, Settlement citadel) {
        OUTLAWS.getOrDefault(citadel.key(), new HashSet<>()).remove(player.getUUID());
    }

    public static boolean isOutlawAt(ServerPlayer player, Settlement citadel) {
        return OUTLAWS.getOrDefault(citadel.key(), Set.of()).contains(player.getUUID());
    }

    private static void outlaw(ServerPlayer player, Settlement citadel, @Nullable Endarch speaker, String topic) {
        OUTLAWS.computeIfAbsent(citadel.key(), k -> ConcurrentHashMap.newKeySet()).add(player.getUUID());
        ServerLevel level = player.level();
        if (speaker == null || !speaker.canSpeak()) speaker = crier(level, citadel, player);
        String line = DialogueBank.get("court").pick(topic, 0, speaker != null ? speaker.job() : "herald", null, level.getRandom(), null);
        if (line != null) {
            String name = speaker != null ? speaker.getName().getString() : "The Court";
            line = DialogueBank.fill(line, Map.of("player", player.getName().getString(), "village", citadel.name(),
                    "name", speaker != null ? speaker.firstName() : "", "title", speaker != null ? speaker.title() : ""));
            shout(level, speaker != null ? speaker : player, Component.literal("<" + name + "> " + line));
        }
        level.playSound(null, player.blockPosition(), SoundEvents.ENDERMAN_SCREAM, SoundSource.HOSTILE, 1.5F, 0.6F);
    }

    /** Says something aloud to every player within earshot. */
    public static void shout(ServerLevel level, net.minecraft.world.entity.Entity from, Component message) {
        for (ServerPlayer p : level.players()) if (p.distanceToSqr(from) < 96 * 96) p.sendSystemMessage(message);
    }

    /** Who cries the alarm: this Citadel's Herald if near, else any Endarch of it. */
    private static @Nullable Endarch crier(ServerLevel level, Settlement citadel, ServerPlayer near) {
        List<Endarch> court = level.getEntitiesOfClass(Endarch.class, near.getBoundingBox().inflate(96),
                e -> e.isAlive() && e.settlement().key().equals(citadel.key()));
        return court.stream().filter(e -> e.job().equals("herald")).findFirst().orElse(court.isEmpty() ? null : court.getFirst());
    }

    /** Every half second: who has crossed into a Citadel, with or without the Eyes, and who has left. */
    public static void tick(MinecraftServer server) {
        if (server.getTickCount() % 10 != 0) return;
        ServerLevel end = server.getLevel(Level.END);
        if (end == null) return;
        Structure structure = end.registryAccess().lookupOrThrow(Registries.STRUCTURE).getValue(EndExpansion.id("citadel"));
        for (ServerPlayer player : server.getPlayerList().getPlayers()) {
            Visit before = INSIDE.get(player.getUUID());
            Visit now = player.level() == end && structure != null ? visit(end, structure, player) : null;
            if (now != null) {
                INSIDE.put(player.getUUID(), now);
                if (player.isCreative() || player.isSpectator() || isOutlawAt(player, now.citadel())) continue;
                if (!carriesEyes(player)) {
                    boolean wasGuest = before != null && before.citadel().key().equals(now.citadel().key());
                    outlaw(player, now.citadel(), null, wasGuest ? "eyes_lost" : "alarm");
                }
            } else if (before != null) {
                if (player.level() == end && before.box().inflatedBy(PARDON_MARGIN).isInside(player.blockPosition())) continue;
                INSIDE.remove(player.getUUID());
                pardon(player, before.citadel());
            }
        }
    }

    private static @Nullable Visit visit(ServerLevel end, Structure structure, ServerPlayer player) {
        StructureStart start = end.structureManager().getStructureAt(player.blockPosition(), structure);
        if (!start.isValid()) return null;
        for (var piece : start.getPieces()) {
            if (piece instanceof ResidentPiece residents) return new Visit(residents.settlement(), start.getBoundingBox());
        }
        return null;
    }

    /** Forget everyone (a new world in the same game, or a test). */
    public static void clear() {
        OUTLAWS.clear();
        INSIDE.clear();
    }
}
