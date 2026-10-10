package dev.endexpansion.entity;

import dev.endexpansion.talk.Bond;
import dev.endexpansion.talk.Conversation;
import dev.endexpansion.talk.DialogueBank;
import dev.endexpansion.talk.Manner;
import dev.endexpansion.talk.Meter;
import dev.endexpansion.talk.StoryBook;
import dev.endexpansion.talk.Tale;
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
import net.minecraft.world.entity.ai.util.DefaultRandomPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.pathfinder.Path;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * A person of the End you can talk to: a Shulkin, a Chorrin, or a member of the Court. Each has a
 * name, a village (or Citadel), a job, a bed or post and a workplace, a personality and a story of
 * their own ({@link StoryBook}), and remembers every player they have talked to ({@link Bond}, and
 * {@link Tale} for the story and the Journal). Right-click to open the conversation.
 *
 * <p>While you talk they stand still and face you, unless that isn't who they are: the shy keep a
 * step of distance, the restless pace, flighty Chorrin blink a hop now and then, and some cut the
 * conversation short (see {@link #leaveReason}): anyone still upset with you for striking them
 * (they turn away), the busy (later for close friends), anyone woken at night, and a proud or busy
 * member of the Court who doesn't think much of you yet.
 */
public abstract class EndFolk extends PathfinderMob implements Settler {
    /** Synced pose flags for the renderer. */
    public static final int TALKING = 1, SLEEPING = 2, WORKING = 4, CLOSED = 8, CARRYING = 16;
    private static final EntityDataAccessor<Byte> FLAGS = SynchedEntityData.defineId(EndFolk.class, EntityDataSerializers.BYTE);
    /** "job|manner", synced so the client can pick animation clips that suit them. */
    private static final EntityDataAccessor<String> MOTION = SynchedEntityData.defineId(EndFolk.class, EntityDataSerializers.STRING);
    private static final Codec<Map<UUID, Bond>> BONDS = Codec.unboundedMap(UUIDUtil.STRING_CODEC, Bond.CODEC);
    private static final Codec<Map<UUID, Tale>> TALES = Codec.unboundedMap(UUIDUtil.STRING_CODEC, Tale.CODEC);
    /** A conversation nobody has touched for this long (five minutes) is over. */
    private static final int MAX_IDLE = 6000;

    protected @Nullable Settlement settlement;
    protected String job = "";
    protected String firstName = "";
    protected @Nullable BlockPos bed, work;
    protected final Map<UUID, Bond> bonds = new HashMap<>();
    protected final Map<UUID, Tale> tales = new HashMap<>();
    /** Their personality and story, by id in their people's story book (chosen once). */
    protected String personality = "", story = "";
    private @Nullable UUID talkingTo;
    private int talkIdle, talkTicks, leaveAt = -1, paceTimer;
    private String leaveReason = "";
    private boolean woken;
    private @Nullable Vec3 talkAnchor;
    /** Players they won't talk to again just yet, having just cut a conversation short (not saved). */
    private final Map<UUID, Snub> snubs = new HashMap<>();
    private @Nullable UUID avoiding;
    private long avoidUntil;
    private int avoidRange;

    private record Snub(String reason, long until) {}
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
        this.personality = StoryBook.get(bank()).pickPersonality(this.job, random).id();
        this.story = "";
    }

    /** Their personality (one is chosen the first time it's needed). */
    public StoryBook.Personality personality() {
        StoryBook book = StoryBook.get(bank());
        if (personality.isEmpty()) personality = book.pickPersonality(job, random).id();
        return book.personality(personality);
    }

    /** Sets their personality by id (tests). */
    public void setPersonality(String id) {
        personality = id;
    }

    public Manner manner() {
        return personality().manner();
    }

    /** Their story (one is chosen the first time it's needed), or null if their people tell none. */
    public StoryBook.@Nullable Story story() {
        StoryBook book = StoryBook.get(bank());
        if (story.isEmpty() || book.story(story) == null) {
            StoryBook.Story pick = book.pickStory(job, random);
            story = pick == null ? "" : pick.id();
        }
        return book.story(story);
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
        builder.define(MOTION, "");
    }

    /** Their job and manner as the client knows them ("archivist|shy"), for the animations. */
    public String motion() {
        return entityData.get(MOTION);
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

    /** What they and a player have been through together: their story so far, and the Journal. */
    public Tale tale(ServerPlayer player) {
        return tales.computeIfAbsent(player.getUUID(), id -> new Tale());
    }

    public void startTalking(ServerPlayer player) {
        woken = isSleeping();
        talkingTo = player.getUUID();
        talkIdle = 0;
        talkTicks = 0;
        paceTimer = 40 + random.nextInt(40);
        talkAnchor = position();
        avoiding = null;
        leaveReason = "";
        leaveAt = -1;
        setFlag(TALKING, true);
        getNavigation().stop();
        planLeave(player);
    }

    public void stopTalking() {
        talkingTo = null;
        leaveAt = -1;
        leaveReason = "";
        setFlag(TALKING, false);
    }

    /**
     * Works out whether (and why) they'll cut this conversation short; called when it starts and
     * after every reply, so an apology or a new level can change their mind. A reason that stays the
     * same keeps its time: the busy don't get busier for being asked another question.
     */
    public void planLeave(ServerPlayer player) {
        String reason = leaveReason(player);
        if (reason.isEmpty()) {
            leaveReason = "";
            leaveAt = -1;
            return;
        }
        if (reason.equals(leaveReason)) return;
        leaveReason = reason;
        boolean friends = meter().level(bond(player).points) >= 6;
        leaveAt = talkTicks + switch (reason) {
            case "dislike" -> 140 + random.nextInt(60);
            case "sleep" -> 300 + random.nextInt(120);
            // the busy make time for close friends, but not all day
            default -> friends ? 2400 + random.nextInt(1200) : 500 + random.nextInt(400);
        };
    }

    /**
     * Why they would walk off, or "" if they'll stay as long as you like: dislike (still upset with
     * you for striking them), sleep (woken at night, unless you are very dear to them), busy (a busy
     * personality: after half a minute or so, or two or three for close friends) or dismissed (the
     * Court: proud and your Favor under 4, or busy and under 6).
     */
    protected String leaveReason(ServerPlayer player) {
        Bond bond = bond(player);
        int level = meter().level(bond.points);
        boolean court = people().equals("court");
        if (!court && bond.grudge > 0) return "dislike";
        if (woken && level < 8) return "sleep";
        return switch (manner()) {
            case BUSY -> court ? level < 6 ? "dismissed" : "" : "busy";
            case PROUD -> level < 4 ? "dismissed" : "";
            default -> "";
        };
    }

    /** Why they are going to cut the conversation short ("" if they aren't). */
    public String leaving() {
        return leaveReason;
    }

    /** Brings their leaving forward to within {@code ticks} (tests). */
    public void hurryLeave(int ticks) {
        if (leaveAt >= 0) leaveAt = Math.min(leaveAt, talkTicks + ticks);
    }

    /** They've had enough: they say so, end the conversation (and go, if they have somewhere to be), and won't talk again just yet. */
    public void walkOff(ServerPlayer partner) {
        String reason = leaveReason.isEmpty() ? "busy" : leaveReason;
        Conversation.walkOff(partner, this, reason);
        stopTalking();
        long now = level().getGameTime();
        snubs.put(partner.getUUID(), new Snub(reason, now + switch (reason) {
            case "dislike" -> 200;
            case "sleep" -> 600;
            default -> 900;
        }));
        leaveWith(partner, reason);
    }

    /**
     * How they go: the busy and the Court step away back to what they were doing; someone upset with
     * you just turns away (and goes on with their day); the woken go back to sleep where they lie.
     */
    protected void leaveWith(ServerPlayer partner, String reason) {
        if (reason.equals("busy") || reason.equals("dismissed")) avoid(partner, 5, 80);
    }

    /** Walk away from a player for a while (the {@link LeaveGoal}). */
    protected void avoid(Player player, int range, int ticks) {
        avoiding = player.getUUID();
        avoidRange = range;
        avoidUntil = level().getGameTime() + ticks;
    }

    /** Whether they are walking away from someone. */
    public boolean isAvoiding() {
        return avoiding != null && level().getGameTime() < avoidUntil;
    }

    /** Why they won't talk to this player again just yet, or null if they will. */
    public @Nullable String snubbedBy(Player player) {
        Snub snub = snubs.get(player.getUUID());
        if (snub == null) return null;
        if (level().getGameTime() >= snub.until()) {
            snubs.remove(player.getUUID());
            return null;
        }
        return snub.reason();
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
        if (tickCount % 40 == 0 && !(this instanceof EndermanThrall)) {
            String motion = job + "|" + manner().name().toLowerCase(java.util.Locale.ROOT);
            if (!motion.equals(entityData.get(MOTION))) entityData.set(MOTION, motion);
        }
        super.customServerAiStep(level);
        if (talkingTo != null) {
            ServerPlayer partner = talkPartner();
            talkTicks++;
            if (partner == null || !partner.isAlive() || partner.distanceToSqr(this) > 100 || ++talkIdle > MAX_IDLE) stopTalking();
            else if (leaveAt >= 0 && talkTicks >= leaveAt) walkOff(partner);
        }
    }

    /** Someone you're talking to holds their ground: they aren't shoved about mid-sentence. */
    @Override
    public boolean isPushable() {
        return !flag(TALKING) && super.isPushable();
    }

    /**
     * One tick of standing (or not standing) still while you talk, by their manner: the steady, busy
     * and proud stay put; the restless pace a step or two; the shy keep a step of distance.
     */
    protected void talkStep(ServerPlayer partner) {
        switch (manner()) {
            case RESTLESS -> pace(partner);
            case SHY -> keepDistance(partner);
            default -> {
                if (!getNavigation().isDone()) getNavigation().stop();
            }
        }
    }

    /** A step or two about the spot where the conversation began, staying close to the player. */
    private void pace(ServerPlayer partner) {
        if (!stayNear()) return;
        if (--paceTimer > 0) return;
        paceTimer = (isChild() ? 30 : 50) + random.nextInt(60);
        Vec3 base = talkAnchor == null ? position() : talkAnchor;
        double r = isChild() ? 2.5 : 1.8;
        for (int i = 0; i < 8; i++) {
            BlockPos spot = BlockPos.containing(base.x + (random.nextDouble() * 2 - 1) * r, base.y, base.z + (random.nextDouble() * 2 - 1) * r);
            double d = partner.distanceToSqr(Vec3.atBottomCenterOf(spot));
            if (d > 25 || d < 2.0) continue;
            if (stepTo(spot, isChild() ? 0.5 : 0.4)) return;
        }
    }

    /** Backs off a little if the player stands too close. */
    private void keepDistance(ServerPlayer partner) {
        if (!stayNear()) return;
        if (--paceTimer > 0) return;
        paceTimer = 20;
        if (distanceToSqr(partner) >= 2.6 * 2.6) return;
        Vec3 away = DefaultRandomPos.getPosAway(this, 3, 1, partner.position());
        if (away != null && partner.distanceToSqr(away) <= 36 && partner.distanceToSqr(away) > distanceToSqr(partner)) {
            stepTo(BlockPos.containing(away), 0.4);
        }
    }

    /** False while a step is under way; a step that strays from the spot where you began talking is cut short. */
    private boolean stayNear() {
        if (getNavigation().isDone()) return true;
        if (talkAnchor != null && position().distanceToSqr(talkAnchor) > 9) getNavigation().stop();
        return false;
    }

    /** A short step, only if the spot itself can be reached in a few blocks (no detours round a tower). */
    private boolean stepTo(BlockPos spot, double speed) {
        Path path = getNavigation().createPath(spot, 0);
        return path != null && path.canReach() && path.getNodeCount() <= 6 && getNavigation().moveTo(path, speed);
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        // the Court counts a blow differently (CitadelLaw.strike), once, not per hit
        if (source.getEntity() instanceof ServerPlayer player && !player.isCreative() && !people().equals("court")) {
            Bond bond = bond(player);
            bond.today(dayNumber());
            bond.points = Math.max(0, bond.points - 15);
            bond.hurtUntil = level.getGameTime() + 6000;
            bond.grudge = Math.min(Bond.MAX_GRUDGE, bond.grudge + 1);
            tale(player).remember(dayNumber(), "You struck " + firstName + ".");
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
        output.store("Tales", TALES, tales);
        output.putString("Personality", personality);
        output.putString("Story", story);
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
        tales.clear();
        tales.putAll(input.read("Tales", TALES).orElse(Map.of()));
        personality = input.getStringOr("Personality", "");
        story = input.getStringOr("Story", "");
    }

    // -- goals ------------------------------------------------------------------------------------

    /** While in a conversation: face the player and stand still (or not, by their manner). */
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
            if (partner == null) return;
            folk.talkStep(partner);
            folk.getLookControl().setLookAt(partner, 30.0F, 30.0F);
        }
    }

    /**
     * Having cut a conversation short to get back to things: away from the player, for a little while. Narrow walkways leave few
     * places to go, so it tries nearer spots too, then straight away along the ground, and goes on
     * until they are clear of the player.
     */
    protected class LeaveGoal extends Goal {
        private int tries;

        public LeaveGoal() {
            setFlags(EnumSet.of(Flag.MOVE));
        }

        @Override
        public boolean canUse() {
            return isAvoiding() && talkingTo == null && getTarget() == null;
        }

        @Override
        public void start() {
            tries = 0;
            if (!walkAway()) avoiding = null;
        }

        @Override
        public boolean canContinueToUse() {
            return isAvoiding() && talkingTo == null && getTarget() == null && (!getNavigation().isDone() || tries < 4);
        }

        @Override
        public void tick() {
            Player from = from();
            if (from == null || !getNavigation().isDone()) return;
            if (distanceToSqr(from) >= avoidRange * avoidRange || ++tries >= 4 || !walkAway()) avoiding = null;
        }

        @Override
        public void stop() {
            avoiding = null;
        }

        private @Nullable Player from() {
            return avoiding == null ? null : level().getPlayerByUUID(avoiding);
        }

        /**
         * Somewhere reachable that ends up further from the player, the further the better: away from
         * them if there's a way, or past them to the door if they've been cornered.
         */
        private boolean walkAway() {
            Player from = from();
            if (from == null) return false;
            double now = distanceToSqr(from), best = now + 4;
            Path chosen = null;
            for (int i = 0; i < 14; i++) {
                int dist = i % 2 == 0 ? avoidRange : Math.max(4, avoidRange * 2 / 3);
                Vec3 spot = i < 8 ? DefaultRandomPos.getPosAway(EndFolk.this, dist, 4, from.position()) : DefaultRandomPos.getPos(EndFolk.this, dist, 4);
                if (spot == null || from.distanceToSqr(spot) <= best) continue;
                Path path = getNavigation().createPath(BlockPos.containing(spot), 0);
                if (path == null || !path.canReach()) continue;
                chosen = path;
                best = from.distanceToSqr(spot);
            }
            if (chosen != null && getNavigation().moveTo(chosen, 0.7)) return true;
            Vec3 dir = position().subtract(from.position()).multiply(1, 0, 1);
            if (dir.lengthSqr() < 1.0E-4) dir = new Vec3(random.nextDouble() - 0.5, 0, random.nextDouble() - 0.5);
            dir = dir.normalize();
            for (int d = avoidRange; d >= 3; d--) {
                for (int dy : new int[] {0, -1, 1, -2, 2}) {
                    BlockPos spot = BlockPos.containing(position().add(dir.scale(d))).above(dy);
                    Path path = getNavigation().createPath(spot, 0);
                    if (path != null && path.canReach() && getNavigation().moveTo(path, 0.7)) return true;
                }
            }
            return false;
        }
    }
}
