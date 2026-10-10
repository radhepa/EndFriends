package dev.endexpansion.talk;

import dev.endexpansion.EndEntities;
import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.entity.EndFolk;
import dev.endexpansion.entity.Endarch;
import dev.endexpansion.entity.EndermanThrall;
import dev.endexpansion.entity.Voidhound;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.ShulkerBoxBlock;
import org.jspecify.annotations.Nullable;

/**
 * The server side of a conversation: what the resident says when you open it, and what happens for
 * each reply (topics), gift or tribute, Court service, and the Lord's hound. Each step sends the
 * whole screen state ({@link TalkPayload}); the client sends back the button pressed
 * ({@link TalkActionPayload}).
 *
 * <p>Closeness grows a little the first time you talk each day and for each topic once a day, and
 * with gifts the resident likes (two a day). The Court counts Favor per Citadel and also sets
 * service tasks: bring what they ask for and Favor grows. At eight eyes of Favor the Lord gives
 * you a Voidhound pup, once per Citadel.
 */
public final class Conversation {
    public static final int GIFTS_PER_DAY = 2;
    public static final int HOUND_LEVEL = 8;
    private static final double REACH = 8.0;

    /** Court service tasks: what to bring, how many, how much Favor, and how the Court names it. */
    public record Task(String id, Item item, int count, int favor, String words) {}

    public static final List<Task> TASKS = List.of(
            task("obsidian", 16, 8, "sixteen blocks of obsidian"),
            task("crying_obsidian", 8, 10, "eight blocks of crying obsidian"),
            task("ender_pearl", 8, 10, "eight ender pearls"),
            task("purpur_block", 32, 7, "thirty-two blocks of purpur"),
            task("end_stone_bricks", 32, 6, "thirty-two end stone bricks"),
            task("end_rod", 8, 8, "eight end rods"),
            task("shulker_shell", 2, 12, "two shulker shells"),
            task("end_crystal", 1, 14, "an end crystal"),
            task("amethyst_shard", 16, 7, "sixteen amethyst shards"),
            task("iron_ingot", 24, 8, "twenty-four iron ingots"),
            task("blaze_rod", 6, 10, "six blaze rods"),
            task("chorus_fruit", 32, 5, "thirty-two chorus fruit for the thralls"));

    private static Task task(String item, int count, int favor, String words) {
        return new Task(item, BuiltInRegistries.ITEM.getValue(Identifier.withDefaultNamespace(item)), count, favor, words);
    }

    private Conversation() {}

    public static void register() {
        PayloadTypeRegistry.clientboundPlay().register(TalkPayload.TYPE, TalkPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(TalkActionPayload.TYPE, TalkActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(TalkActionPayload.TYPE, (payload, context) -> act(context.player(), payload));
    }

    // -- opening ----------------------------------------------------------------------------------

    public static void open(ServerPlayer player, EndFolk folk) {
        if (folk.getTarget() != null) return;
        boolean court = folk instanceof Endarch;
        if (court && !CitadelLaw.isGuest(player, folk)) {
            if (!CitadelLaw.isOutlaw(player, folk)) narrate(player, folk.getName().getString() + " will not speak with one who does not bear the Eyes.");
            return;
        }
        ServerLevel level = player.level();
        Bond bond = folk.bond(player);
        bond.today(folk.dayNumber());
        int before = folk.meter().level(bond.points);
        String topic;
        if (!bond.met) {
            topic = "first_meeting";
            bond.met = true;
        } else if (bond.hurtUntil > level.getGameTime()) {
            topic = court ? "greeting" : "hurt";
        } else if (folk.isSleeping()) {
            topic = "night";
        } else if (!court && carriesShulkerBox(player) && folk.getRandom().nextInt(5) < 3) {
            topic = "shulker_box";
        } else if (!court && CitadelLaw.carriesEyes(player) && folk.getRandom().nextInt(2) == 0) {
            topic = "eyes";
        } else {
            topic = "greeting";
        }
        String status = "";
        if (!bond.greeted) {
            bond.greeted = true;
            int gain = court ? 2 : 4;
            gain(folk, bond, gain);
            status = (court ? "An audience today: Favor +" : "First words today: +") + gain;
        }
        folk.startTalking(player);
        send(player, folk, bond, say(folk, player, topic, bond), status, before, true);
    }

    /** An Enderman thrall won't talk: a line of narration instead. */
    public static void thrall(ServerPlayer player, EndermanThrall thrall) {
        String line = DialogueBank.get("court").pick("thrall", 0, null, null, thrall.getRandom(), thrall.lastLine);
        if (line == null) return;
        thrall.lastLine = line;
        narrate(player, line);
    }

    private static void narrate(ServerPlayer player, String text) {
        player.sendSystemMessage(Component.literal(text).withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
    }

    // -- replies ----------------------------------------------------------------------------------

    static void act(ServerPlayer player, TalkActionPayload action) {
        if (!(player.level().getEntity(action.entityId()) instanceof EndFolk folk) || !folk.getUUID().equals(action.id())
                || !folk.isAlive() || folk.distanceToSqr(player) > REACH * REACH || !folk.isTalkingTo(player)) return;
        if (action.action().equals("goodbye")) {
            folk.stopTalking();
            return;
        }
        boolean court = folk instanceof Endarch;
        if (court && !CitadelLaw.isGuest(player, folk)) {
            folk.stopTalking();
            return;
        }
        folk.keepTalking();
        Bond bond = folk.bond(player);
        bond.today(folk.dayNumber());
        int before = folk.meter().level(bond.points);
        String said, status = "";
        switch (action.action()) {
            case "talk" -> said = say(folk, player, "greeting", bond);
            case "gift" -> {
                String[] out = gift(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            case "service" -> {
                String[] out = service(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            case "hound" -> {
                String[] out = hound(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            default -> {
                if (!topics(folk).contains(action.action())) return;
                String topic = action.action().equals("peoples") ? (folk.getRandom().nextBoolean() ? "shulkin" : "chorrin") : action.action();
                said = say(folk, player, topic, bond);
                if (bond.topics.add(action.action())) {
                    int gain = court ? 1 : action.action().equals("chat") ? 4 : 3;
                    gain(folk, bond, gain);
                    status = (court ? "Favor +" : "+") + gain;
                } else {
                    status = "You have talked about that today.";
                }
            }
        }
        send(player, folk, bond, said, status, before, false);
    }

    private static String[] gift(ServerPlayer player, EndFolk folk, Bond bond) {
        boolean court = folk instanceof Endarch;
        String prefix = court ? "tribute_" : "gift_";
        ItemStack held = player.getMainHandItem();
        if (held.isEmpty()) return new String[] {folk.lastLine, "Hold something in your hand to " + (court ? "offer it." : "give it.")};
        if (bond.gifts >= GIFTS_PER_DAY) return new String[] {say(folk, player, prefix + "limit", bond), "No more " + (court ? "tribute" : "gifts") + " today."};
        String taste = DialogueBank.get(folk.bank()).taste(held);
        int points = switch (taste) {
            case "loved" -> court ? 8 : 25;
            case "liked" -> court ? 4 : 12;
            case "disliked" -> court ? -3 : -8;
            default -> court ? 1 : 4;
        };
        String name = held.getHoverName().getString();
        if (!player.hasInfiniteMaterials()) held.shrink(1);
        bond.gifts++;
        gain(folk, bond, points);
        player.level().playSound(null, folk.blockPosition(), SoundEvents.ITEM_PICKUP, SoundSource.NEUTRAL, 0.6F, 1.1F);
        String verdict = switch (taste) {
            case "loved" -> "They loved the " + name + "!";
            case "liked" -> "They liked the " + name + ".";
            case "disliked" -> "They didn't like the " + name + ".";
            default -> "They took the " + name + ".";
        };
        return new String[] {say(folk, player, prefix + taste, bond), verdict + " " + (points >= 0 ? "+" : "") + points};
    }

    private static String[] service(ServerPlayer player, EndFolk folk, Bond bond) {
        Task task = task(bond.task);
        if (task == null) {
            task = TASKS.get(folk.getRandom().nextInt(TASKS.size()));
            bond.task = task.id();
            return new String[] {say(folk, player, "service_offer", bond), "The Court asks for " + task.words() + "."};
        }
        if (count(player, task.item()) >= task.count() || player.hasInfiniteMaterials()) {
            if (!player.hasInfiniteMaterials()) take(player, task.item(), task.count());
            gain(folk, bond, task.favor());
            String said = say(folk, player, "service_done", bond);
            bond.task = "";
            return new String[] {said, "Service done: Favor +" + task.favor()};
        }
        return new String[] {say(folk, player, "service_waiting", bond),
                "Bring " + task.words() + " (you have " + count(player, task.item()) + ")."};
    }

    private static String[] hound(ServerPlayer player, EndFolk folk, Bond bond) {
        int level = folk.meter().level(bond.points);
        if (bond.hound) return new String[] {say(folk, player, "hound_already", bond), "This Court has given you its hound."};
        if (level < HOUND_LEVEL) return new String[] {say(folk, player, "hound_low", bond), "The Lord gives a hound at " + HOUND_LEVEL + " eyes of Favor."};
        Voidhound pup = EndEntities.VOIDHOUND.create(player.level(), EntitySpawnReason.MOB_SUMMONED);
        if (pup == null) return new String[] {folk.lastLine, ""};
        pup.snapTo(player.getX(), player.getY(), player.getZ(), player.getYRot(), 0.0F);
        pup.makePup(player);
        player.level().addFreshEntity(pup);
        bond.hound = true;
        return new String[] {say(folk, player, "hound_given", bond), "A Voidhound pup is yours."};
    }

    // -- helpers ----------------------------------------------------------------------------------

    /** The replies offered by each kind of person. */
    public static List<String> topics(EndFolk folk) {
        if (folk instanceof Endarch e) {
            List<String> out = new ArrayList<>(List.of("chat", "law", "dragon", "thralls", "peoples", "secret", "service"));
            if (e.job().equals("lord")) out.add("hound");
            return out;
        }
        String own = folk.people().equals("shulkin") ? "ancestors" : "void";
        return folk.isChild()
                ? List.of("chat", "play", "dragon", "village", "other", "court", own, "overworld")
                : List.of("chat", "dragon", "work", "village", "other", "court", own, "overworld");
    }

    private static String label(EndFolk folk, String topic, Bond bond) {
        return switch (topic) {
            case "chat" -> folk instanceof Endarch ? "Address them" : "Chat";
            case "play" -> "Play together";
            case "dragon" -> folk instanceof Endarch ? "Speak of the Dragon" : "Ask about the Dragon";
            case "work" -> "Ask about their work";
            case "village" -> "Ask about home";
            case "other" -> folk.people().equals("shulkin") ? "Ask about the Chorrin" : "Ask about the Shulkin";
            case "court" -> "Ask about the Court";
            case "ancestors" -> "Ask about the old shells";
            case "void" -> "Ask about the void";
            case "overworld" -> "Tell of the Overworld";
            case "law" -> "Ask about the law";
            case "thralls" -> "Ask about the thralls";
            case "peoples" -> "Ask of the other peoples";
            case "secret" -> "Ask where Endarchs come from";
            case "service" -> {
                Task t = task(bond.task);
                yield t == null ? "Offer your service" : "Deliver " + t.words();
            }
            case "hound" -> "Ask for a hound";
            default -> topic;
        };
    }

    private static @Nullable Task task(String id) {
        for (Task t : TASKS) if (t.id().equals(id)) return t;
        return null;
    }

    private static int count(ServerPlayer player, Item item) {
        int n = 0;
        for (ItemStack s : player.getInventory()) if (s.is(item)) n += s.getCount();
        return n;
    }

    private static void take(ServerPlayer player, Item item, int count) {
        for (ItemStack s : player.getInventory()) {
            if (count <= 0) return;
            if (!s.is(item)) continue;
            int used = Math.min(count, s.getCount());
            s.shrink(used);
            count -= used;
        }
    }

    public static boolean carriesShulkerBox(ServerPlayer player) {
        return player.getInventory().contains(s -> s.getItem() instanceof BlockItem b && b.getBlock() instanceof ShulkerBoxBlock);
    }

    private static void gain(EndFolk folk, Bond bond, int points) {
        bond.points = Math.clamp(bond.points + points, 0, folk.meter().cap());
    }

    /** A line on a topic at the bond's level, placeholders filled. */
    static String say(EndFolk folk, ServerPlayer player, String topic, Bond bond) {
        DialogueBank bank = DialogueBank.get(folk.bank());
        int level = folk.meter().level(bond.points);
        boolean court = folk.people().equals("court");
        String line = bank.pick(topic, level, court ? folk.job() : null, court ? null : folk.job(), folk.getRandom(), folk.lastLine);
        if (line == null) line = bank.pick("greeting", level, court ? folk.job() : null, null, folk.getRandom(), folk.lastLine);
        if (line == null) line = "...";
        String filled = DialogueBank.fill(line, vars(folk, player, bond));
        folk.lastLine = filled;
        return filled;
    }

    private static Map<String, String> vars(EndFolk folk, ServerPlayer player, Bond bond) {
        Map<String, String> v = new HashMap<>();
        v.put("player", player.getName().getString());
        v.put("name", folk.firstName());
        v.put("village", folk.settlement().name());
        v.put("job", folk.title().toLowerCase(java.util.Locale.ROOT));
        v.put("title", folk.title());
        v.put("neighbour", neighbour(folk));
        Task t = task(bond.task);
        v.put("task", t == null ? "what the Court asks" : t.words());
        v.put("lord", lord(folk));
        return v;
    }

    /** Another resident of the same village by first name (made up if nobody is near). */
    private static String neighbour(EndFolk folk) {
        var near = folk.level().getEntitiesOfClass(EndFolk.class, folk.getBoundingBox().inflate(64),
                o -> o != folk && !o.firstName().isEmpty() && o.people().equals(folk.people()) && o.settlement().key().equals(folk.settlement().key()));
        if (!near.isEmpty()) return near.get(folk.getRandom().nextInt(near.size())).firstName();
        var names = DialogueBank.get(folk.people()).names();
        return names.isEmpty() ? "someone" : names.get(folk.getRandom().nextInt(names.size()));
    }

    private static String lord(EndFolk folk) {
        if (folk instanceof Endarch e && e.job().equals("lord")) return e.firstName();
        var lords = folk.level().getEntitiesOfClass(Endarch.class, folk.getBoundingBox().inflate(128),
                o -> o.job().equals("lord") && o.settlement().key().equals(folk.settlement().key()));
        if (!lords.isEmpty()) return lords.getFirst().firstName();
        RandomSource r = RandomSource.create(folk.settlement().key().hashCode());
        var names = DialogueBank.get("court").names();
        return names.isEmpty() ? "of the Citadel" : names.get(r.nextInt(names.size()));
    }

    private static void send(ServerPlayer player, EndFolk folk, Bond bond, String dialogue, String status, int levelBefore, boolean opening) {
        Meter meter = folk.meter();
        int level = meter.level(bond.points);
        boolean levelUp = level > levelBefore;
        DialogueBank bank = DialogueBank.get(folk.bank());
        if (levelUp) {
            String up = bank.pick("level_up", level, folk.people().equals("court") ? folk.job() : null, null, folk.getRandom(), null);
            if (up != null) dialogue = dialogue + " " + DialogueBank.fill(up, vars(folk, player, bond));
        }
        List<TalkPayload.Choice> choices = new ArrayList<>();
        for (String topic : topics(folk)) {
            boolean enabled = true;
            String hint = "";
            if (topic.equals("hound") && !bond.hound && level < HOUND_LEVEL) hint = "The Lord gives a hound at " + HOUND_LEVEL + " eyes of Favor.";
            choices.add(new TalkPayload.Choice(topic, label(folk, topic, bond), enabled, hint));
        }
        ServerPlayNetworking.send(player, new TalkPayload(folk.getId(), folk.getUUID(), folk.getName().getString(), folk.title(),
                folk.settlement().name(), folk.bank(), meter.id, level, bank.levelName(level), bond.points, meter.floor(level),
                meter.next(level), dialogue, status, choices, Math.max(0, GIFTS_PER_DAY - bond.gifts),
                folk instanceof Endarch ? "Tribute" : "Gift", levelUp, opening));
    }
}
