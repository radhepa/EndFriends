package dev.endexpansion.entity;

import dev.endexpansion.talk.Bond;
import dev.endexpansion.talk.Conversation;
import dev.endexpansion.talk.DialogueBank;
import dev.endexpansion.talk.Meter;
import dev.endexpansion.world.Settlement;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.UUIDUtil;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jspecify.annotations.Nullable;

/**
 * A person of the End you can talk to: a Shulkin, a Chorrin, or a member of the Court. Each has a
 * name, a village (or Citadel), a job, a bed or post and a workplace, and remembers every player
 * they have talked to ({@link Bond}). Right-click to open the conversation.
 */
public abstract class EndFolk extends PathfinderMob implements Settler {
    /** Synced pose flags for the renderer. */
    public static final int TALKING = 1, SLEEPING = 2, WORKING = 4, CLOSED = 8, CARRYING = 16;
    private static final EntityDataAccessor<Byte> FLAGS = SynchedEntityData.defineId(EndFolk.class, EntityDataSerializers.BYTE);
    private static final Codec<Map<UUID, Bond>> BONDS = Codec.unboundedMap(UUIDUtil.STRING_CODEC, Bond.CODEC);

    protected @Nullable Settlement settlement;
    protected String job = "";
    protected String firstName = "";
    protected @Nullable BlockPos bed, work;
    protected final Map<UUID, Bond> bonds = new HashMap<>();
    private @Nullable UUID talkingTo;
    private int talkIdle;
    /** The last line said, so the next one isn't the same. */
    public String lastLine = "";

    protected EndFolk(EntityType<? extends EndFolk> type, Level level) {
        super(type, level);
        this.setPersistenceRequired();
    }

    // -- who they are -----------------------------------------------------------------------------

    /** shulkin, chorrin or court. */
    public abstract String people();

    /** The dialogue bank that speaks for them. */
    public String bank() {
        return isChild() ? people() + "_child" : people();
    }

    public boolean isChild() {
        return false;
    }

    public Meter meter() {
        return Meter.BLOSSOM;
    }

    /** The job a resident from a spawn egg gets. */
    protected abstract String defaultJob();

    /** Their job as shown under their name. */
    public abstract String title();

    /** Their whole name, made once from their first name. */
    protected abstract String fullName(String first, RandomSource random);

    public String job() {
        return job;
    }

    public String firstName() {
        return firstName;
    }

    @Override
    public Settlement settlement() {
        if (settlement == null) settlement = Settlement.wild(people(), blockPosition(), random);
        return settlement;
    }

    public @Nullable BlockPos bed() {
        return bed;
    }

    public @Nullable BlockPos work() {
        return work;
    }

    @Override
    public void settle(Settlement settlement, String job, BlockPos home, @Nullable BlockPos work) {
        this.settlement = settlement;
        this.job = job.isEmpty() ? defaultJob() : job;
        this.bed = home;
        this.work = work;
        this.setHomeTo(settlement.isWild() ? home : settlement.center(), homeRadius());
        this.name(random);
    }

    /** How far from the village centre they wander. */
    protected int homeRadius() {
        return 64;
    }

    protected void name(RandomSource random) {
        var names = DialogueBank.get(bank()).names();
        firstName = names.isEmpty() ? "Nameless" : names.get(random.nextInt(names.size()));
        setCustomName(Component.literal(fullName(firstName, random)));
    }

    @Override
    public @Nullable SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
                                                  @Nullable SpawnGroupData data) {
        SpawnGroupData out = super.finalizeSpawn(level, difficulty, reason, data);
        if (reason != EntitySpawnReason.STRUCTURE && settlement == null) {
            // a spawn egg or a command: a stranger from somewhere else, at home where they stand
            settle(Settlement.wild(people(), blockPosition(), random), "", blockPosition(), null);
            setHomeTo(blockPosition(), 16);
        }
        return out;
    }

    // -- pose flags -------------------------------------------------------------------------------

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(FLAGS, (byte) 0);
    }

    public boolean flag(int flag) {
        return (entityData.get(FLAGS) & flag) != 0;
    }

    protected void setFlag(int flag, boolean on) {
        byte now = entityData.get(FLAGS);
        byte next = (byte) (on ? now | flag : now & ~flag);
        if (next != now) entityData.set(FLAGS, next);
    }

    public boolean isSleeping() {
        return flag(SLEEPING);
    }

    // -- talking ----------------------------------------------------------------------------------

    /** Their bond with a player (the Court keeps one per Citadel instead, see {@code Endarch}). */
    public Bond bond(ServerPlayer player) {
        return bonds.computeIfAbsent(player.getUUID(), id -> new Bond());
    }

    public void startTalking(ServerPlayer player) {
        talkingTo = player.getUUID();
        talkIdle = 0;
        setFlag(TALKING, true);
        getNavigation().stop();
    }

    public void stopTalking() {
        talkingTo = null;
        setFlag(TALKING, false);
    }

    /** Called on every reply, so a conversation left open doesn't hold them forever. */
    public void keepTalking() {
        talkIdle = 0;
    }

    public @Nullable ServerPlayer talkPartner() {
        if (talkingTo == null || !(level() instanceof ServerLevel server)) return null;
        return server.getPlayerByUUID(talkingTo) instanceof ServerPlayer p ? p : null;
    }

    public boolean isTalkingTo(Player player) {
        return player.getUUID().equals(talkingTo);
    }

    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (hand != InteractionHand.MAIN_HAND || !isAlive()) return InteractionResult.PASS;
        if (player instanceof ServerPlayer sp) Conversation.open(sp, this);
        return InteractionResult.SUCCESS;
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (talkingTo != null) {
            ServerPlayer partner = talkPartner();
            if (partner == null || !partner.isAlive() || partner.distanceToSqr(this) > 100 || ++talkIdle > 1200) stopTalking();
        }
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        // the Court counts a blow differently (CitadelLaw.strike), once, not per hit
        if (source.getEntity() instanceof ServerPlayer player && !player.isCreative() && !people().equals("court")) {
            Bond bond = bond(player);
            bond.points = Math.max(0, bond.points - 15);
            bond.hurtUntil = level.getGameTime() + 6000;
            if (isTalkingTo(player)) stopTalking();
        }
        return super.hurtServer(level, source, damage);
    }

    /** The time of day on the overworld clock (the End's own sky never changes), 0-23999. */
    public long dayTime() {
        return Math.floorMod(level().getOverworldClockTime(), 24000L);
    }

    public long dayNumber() {
        return Math.floorDiv(level().getOverworldClockTime(), 24000L);
    }

    // -- persistence ------------------------------------------------------------------------------

    @Override
    public boolean removeWhenFarAway(double distSqr) {
        return false;
    }

    @Override
    public boolean requiresCustomPersistence() {
        return true;
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        if (settlement != null) {
            output.putString("VillageKind", settlement.kind());
            output.store("VillageCenter", BlockPos.CODEC, settlement.center());
            output.putString("VillageName", settlement.name());
        }
        output.putString("Job", job);
        output.putString("FirstName", firstName);
        if (bed != null) output.store("Bed", BlockPos.CODEC, bed);
        if (work != null) output.store("Work", BlockPos.CODEC, work);
        output.store("Bonds", BONDS, bonds);
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        settlement = Settlement.read(input.getStringOr("VillageKind", ""), input.read("VillageCenter", BlockPos.CODEC).orElse(null),
                input.getStringOr("VillageName", ""));
        job = input.getStringOr("Job", defaultJob());
        firstName = input.getStringOr("FirstName", "");
        bed = input.read("Bed", BlockPos.CODEC).orElse(null);
        work = input.read("Work", BlockPos.CODEC).orElse(null);
        bonds.clear();
        bonds.putAll(input.read("Bonds", BONDS).orElse(Map.of()));
    }

    // -- goals ------------------------------------------------------------------------------------

    /** While in a conversation: stand still and look at the player. */
    protected static class TalkGoal extends Goal {
        private final EndFolk folk;

        public TalkGoal(EndFolk folk) {
            this.folk = folk;
            setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK, Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            return folk.talkingTo != null && folk.getTarget() == null;
        }

        @Override
        public void start() {
            folk.getNavigation().stop();
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void tick() {
            ServerPlayer partner = folk.talkPartner();
            if (partner != null) folk.getLookControl().setLookAt(partner, 30.0F, 30.0F);
        }
    }
}
