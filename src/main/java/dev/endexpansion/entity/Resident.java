package dev.endexpansion.entity;

import java.util.EnumSet;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.OpenDoorGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.util.DefaultRandomPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.pathfinder.Path;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * A Shulkin or Chorrin villager (or one of their children), living by the overworld clock: work
 * (or play) by day, the plaza in the evening, their niche or nest at night. Doors open for them.
 * Where no player is watching, a resident who can't find the way simply turns up where they meant
 * to be, so nobody spends the night stuck on a bridge.
 */
public abstract class Resident extends EndFolk {
    /** Work (play) from early morning, the plaza in the evening, bed from nightfall to before dawn. */
    static final long WORK_FROM = 1000, EVENING = 11000, NIGHT = 13000, DAWN = 23500;

    protected Resident(EntityType<? extends Resident> type, Level level) {
        super(type, level);
        getNavigation().setCanOpenDoors(true);
    }

    public static AttributeSupplier.Builder residentAttributes(double health) {
        return createMobAttributes()
                .add(Attributes.MAX_HEALTH, health)
                .add(Attributes.MOVEMENT_SPEED, 0.5)
                .add(Attributes.FOLLOW_RANGE, 64.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new TalkGoal(this));
        goalSelector.addGoal(2, new SleepGoal());
        goalSelector.addGoal(3, new RoutineGoal());
        goalSelector.addGoal(4, new OpenDoorGoal(this, true));
        goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, isChild() ? 0.75 : 0.55));
        goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
    }

    public boolean isNight() {
        long t = dayTime();
        return t >= NIGHT && t < DAWN;
    }

    /** Where the routine takes them now: work (children: the plaza to play), or the plaza in the evening. */
    protected @Nullable BlockPos routineTarget() {
        long t = dayTime();
        if (t >= NIGHT && t < DAWN) return null;
        if (t >= EVENING) return settlement().isWild() ? null : settlement().center().above();
        if (t >= WORK_FROM) return work != null ? work : settlement().isWild() ? null : settlement().center().above();
        return null;
    }

    /** No one near enough to see them: they can just be where they meant to go. */
    boolean unwatched(ServerLevel level) {
        return level.getNearestPlayer(this, 40.0) == null;
    }

    /** Walk toward a spot, a stretch at a time when it is too far for one path. */
    boolean travelTo(BlockPos target, double speed) {
        Path path = getNavigation().createPath(target, 1);
        if (path != null && getNavigation().moveTo(path, speed)) return true;
        Vec3 closer = DefaultRandomPos.getPosTowards(this, 16, 7, Vec3.atBottomCenterOf(target), Math.PI / 2);
        return closer != null && getNavigation().moveTo(closer.x, closer.y, closer.z, speed);
    }

    void arrive(BlockPos spot) {
        getNavigation().stop();
        snapTo(spot.getX() + 0.5, spot.getY(), spot.getZ() + 0.5, getYRot(), getXRot());
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (isSleeping() && (!isNight() || getTarget() != null || hurtTime > 0)) setFlag(SLEEPING, false);
    }

    /** At night: home to their niche or nest, and sleep there till dawn. */
    class SleepGoal extends Goal {
        private int retry, lost;

        SleepGoal() {
            setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK, Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            return bed != null && isNight() && !flag(TALKING) && hurtTime == 0;
        }

        @Override
        public boolean canContinueToUse() {
            return canUse();
        }

        @Override
        public void start() {
            retry = 0;
            lost = 0;
            travelTo(bed, 0.6);
        }

        @Override
        public void stop() {
            setFlag(SLEEPING, false);
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void tick() {
            if (isSleeping()) return;
            Vec3 spot = Vec3.atBottomCenterOf(bed);
            if (position().distanceToSqr(spot) < 1.6) {
                arrive(bed);
                setFlag(SLEEPING, true);
                return;
            }
            lost++;
            if (getNavigation().isDone() && ++retry % 40 == 0) travelTo(bed, 0.6);
            if (lost > 600 && level() instanceof ServerLevel server && unwatched(server)) {
                arrive(bed);
                setFlag(SLEEPING, true);
            }
        }
    }

    /** By day at work (children at play round the plaza), in the evening at the plaza. */
    class RoutineGoal extends Goal {
        private @Nullable BlockPos target;
        private int retry, lost, wander;

        RoutineGoal() {
            setFlags(EnumSet.of(Flag.MOVE));
        }

        @Override
        public boolean canUse() {
            if (flag(TALKING) || isSleeping()) return false;
            BlockPos t = routineTarget();
            // most of the time; now and then the stroll goal gets a turn
            return t != null && (position().distanceToSqr(Vec3.atBottomCenterOf(t)) > 36 || getRandom().nextInt(isChild() ? 6 : 3) != 0);
        }

        @Override
        public boolean canContinueToUse() {
            return !flag(TALKING) && target != null && target.equals(routineTarget());
        }

        @Override
        public void start() {
            target = routineTarget();
            retry = 0;
            lost = 0;
            wander = 0;
            if (target != null) travelTo(target, isChild() ? 0.7 : 0.6);
        }

        @Override
        public void stop() {
            setFlag(WORKING, false);
            target = null;
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void tick() {
            if (target == null) return;
            double d = position().distanceToSqr(Vec3.atBottomCenterOf(target));
            // a workplace is a spot; the plaza is anywhere near its middle
            boolean plaza = settlement != null && target.equals(settlement.center().above());
            if (d < (plaza ? 36 : 6.25)) {
                lost = 0;
                boolean atWork = work != null && target.equals(work) && !isChild();
                setFlag(WORKING, atWork);
                // a few steps about now and then, then back
                if (++wander > 160 + getRandom().nextInt(400)) {
                    wander = 0;
                    Vec3 near = DefaultRandomPos.getPos(Resident.this, atWork ? 4 : 8, 2);
                    if (near != null) getNavigation().moveTo(near.x, near.y, near.z, 0.5);
                }
                return;
            }
            setFlag(WORKING, false);
            lost++;
            if (getNavigation().isDone() && ++retry % 40 == 0) travelTo(target, isChild() ? 0.7 : 0.6);
            if (!plaza && lost > 900 && level() instanceof ServerLevel server && unwatched(server)) arrive(target);
        }
    }
}
