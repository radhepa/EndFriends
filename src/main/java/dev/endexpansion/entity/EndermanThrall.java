package dev.endexpansion.entity;

import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.court.CourtFavor;
import dev.endexpansion.talk.Bond;
import dev.endexpansion.talk.Conversation;
import java.util.EnumSet;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.util.DefaultRandomPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * An Enderman in a Citadel's service, in a purpur bond-collar: it hauls the Court's stone about the
 * thrall yards, never speaks and won't meet your eyes. It fights for the Court like any Endarch.
 */
public class EndermanThrall extends EndFolk {
    public EndermanThrall(EntityType<? extends EndermanThrall> type, Level level) {
        super(type, level);
        this.xpReward = 5;
    }

    public static AttributeSupplier.Builder attributes() {
        return createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0)
                .add(Attributes.ATTACK_DAMAGE, 7.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.FOLLOW_RANGE, 48.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.2, false));
        goalSelector.addGoal(4, new HaulGoal());
        goalSelector.addGoal(5, new MoveTowardsRestrictionGoal(this, 0.6));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers(Endarch.class, EndermanThrall.class));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, false, (target, level) -> CitadelLaw.isOutlaw(target, this)));
    }

    @Override public String people() { return "court"; }
    @Override protected String defaultJob() { return "thrall"; }
    @Override public String title() { return "Thrall"; }
    @Override protected String fullName(String first, RandomSource random) { return "Enderman Thrall"; }
    @Override protected int homeRadius() { return 10; }

    @Override
    public void settle(dev.endexpansion.world.Settlement settlement, String job, BlockPos home, @Nullable BlockPos work) {
        super.settle(settlement, job, home, work);
        setHomeTo(home, homeRadius());
        setCustomName(null);
    }

    @Override
    public Bond bond(ServerPlayer player) {
        return CourtFavor.get(player.level().getServer()).bond(settlement().key(), player.getUUID());
    }

    /** It doesn't talk: you get a glimpse of it instead. */
    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (hand != InteractionHand.MAIN_HAND) return InteractionResult.PASS;
        if (player instanceof ServerPlayer sp) Conversation.thrall(sp, this);
        return InteractionResult.SUCCESS;
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        if (source.getEntity() instanceof ServerPlayer player) CitadelLaw.strike(player, this);
        return super.hurtServer(level, source, damage);
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        // a target the law no longer names is let go, unless it struck first
        if (getTarget() instanceof ServerPlayer p && !CitadelLaw.isOutlaw(p, this) && getLastHurtByMob() != p) setTarget(null);
        if (getTarget() != null) setFlag(CARRYING, false);
    }

    public boolean isCarrying() {
        return flag(CARRYING);
    }

    @Override protected @Nullable SoundEvent getAmbientSound() { return getTarget() != null ? SoundEvents.ENDERMAN_SCREAM : SoundEvents.ENDERMAN_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.ENDERMAN_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.ENDERMAN_DEATH; }
    @Override public int getAmbientSoundInterval() { return 400; }

    /** Carries a block of the Court's stone to somewhere else in the yard, sets it down, fetches another. */
    class HaulGoal extends Goal {
        private int pause;

        HaulGoal() {
            setFlags(EnumSet.of(Flag.MOVE));
        }

        @Override
        public boolean canUse() {
            return getTarget() == null && getRandom().nextInt(60) == 0;
        }

        @Override
        public boolean canContinueToUse() {
            return getTarget() == null && (!getNavigation().isDone() || pause > 0);
        }

        @Override
        public void start() {
            pause = 0;
            Vec3 to = DefaultRandomPos.getPos(EndermanThrall.this, 8, 3);
            if (to != null) getNavigation().moveTo(to.x, to.y, to.z, 0.55);
        }

        @Override
        public void tick() {
            if (getNavigation().isDone() && pause == 0) {
                pause = 40 + getRandom().nextInt(60);
                setFlag(CARRYING, !flag(CARRYING));   // set it down, or pick one up
            }
            if (pause > 0) pause--;
        }
    }
}
