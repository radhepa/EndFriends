package dev.endexpansion.entity;

import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.court.CourtFavor;
import dev.endexpansion.talk.Bond;
import dev.endexpansion.talk.DialogueBank;
import dev.endexpansion.talk.Meter;
import java.util.Map;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * An Endarch of the Court: the Lord, a Voidmarshal (also the Herald, Seer and Steward, who share
 * their rank) or a Riftguard. They keep their posts, speak with guests who bear Enderman Eyes, and
 * fall on outlaws (see {@link CitadelLaw}). Riftguards rift-step behind whoever they fight and
 * slip aside from arrows. Favor is kept per Citadel, not per Endarch.
 */
public class Endarch extends EndFolk {
    public enum Rank { LORD, MARSHAL, RIFTGUARD }

    private final Rank rank;
    private int riftCooldown, cryCooldown;

    public Endarch(EntityType<? extends Endarch> type, Level level, Rank rank) {
        super(type, level);
        this.rank = rank;
        this.xpReward = rank == Rank.LORD ? 50 : rank == Rank.MARSHAL ? 30 : 20;
    }

    public static AttributeSupplier.Builder attributes(Rank rank) {
        return createMobAttributes()
                .add(Attributes.MAX_HEALTH, switch (rank) { case LORD -> 160.0; case MARSHAL -> 100.0; case RIFTGUARD -> 70.0; })
                .add(Attributes.ATTACK_DAMAGE, switch (rank) { case LORD -> 14.0; case MARSHAL -> 12.0; case RIFTGUARD -> 10.0; })
                .add(Attributes.ARMOR, switch (rank) { case LORD -> 10.0; case MARSHAL -> 12.0; case RIFTGUARD -> 6.0; })
                .add(Attributes.MOVEMENT_SPEED, rank == Rank.RIFTGUARD ? 0.33 : 0.3)
                .add(Attributes.KNOCKBACK_RESISTANCE, rank == Rank.RIFTGUARD ? 0.5 : 0.8)
                .add(Attributes.FOLLOW_RANGE, 48.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    public Rank rank() {
        return rank;
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new TalkGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15, true));
        goalSelector.addGoal(3, new LeaveGoal());
        goalSelector.addGoal(5, new MoveTowardsRestrictionGoal(this, 0.6));
        goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, 0.45, 0.004F));
        goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 10.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers(Endarch.class, EndermanThrall.class));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, false, (target, level) -> CitadelLaw.isOutlaw(target, this)));
    }

    @Override
    public String people() {
        return "court";
    }

    @Override
    public Meter meter() {
        return Meter.EYE;
    }

    @Override
    protected String defaultJob() {
        return switch (rank) { case LORD -> "lord"; case MARSHAL -> "marshal"; case RIFTGUARD -> "riftguard"; };
    }

    @Override
    public String title() {
        return switch (job) {
            case "lord" -> "Lord";
            case "herald" -> "Herald";
            case "seer" -> "Seer";
            case "steward" -> "Steward";
            case "riftguard" -> "Riftguard";
            default -> "Voidmarshal";
        };
    }

    @Override
    protected String fullName(String first, RandomSource random) {
        return title() + " " + first;
    }

    /** Posts: the Lord keeps the throne, the Herald the gate; Riftguards range the Citadel. */
    @Override
    protected int homeRadius() {
        return switch (job) {
            case "lord", "herald" -> 3;
            case "seer" -> 4;
            case "steward" -> 6;
            case "riftguard" -> 20;
            default -> 10;
        };
    }

    @Override
    public void settle(dev.endexpansion.world.Settlement settlement, String job, net.minecraft.core.BlockPos home,
                       net.minecraft.core.BlockPos work) {
        super.settle(settlement, job, home, work);
        setHomeTo(home, homeRadius());
    }

    /** Everyone speaks but in battle. */
    public boolean canSpeak() {
        return isAlive();
    }

    /** One Citadel, one Favor: shared by every member of its Court. */
    @Override
    public Bond bond(ServerPlayer player) {
        return CourtFavor.get(player.level().getServer()).bond(settlement().key(), player.getUUID());
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        if (rank == Rank.RIFTGUARD && source.is(DamageTypeTags.IS_PROJECTILE) && random.nextFloat() < 0.65F && blink(8)) return false;
        if (source.getEntity() instanceof ServerPlayer player) CitadelLaw.strike(player, this);
        return super.hurtServer(level, source, damage);
    }

    /** A short rift-step to somewhere near. */
    private boolean blink(int range) {
        for (int i = 0; i < 16; i++) {
            double x = getX() + (random.nextDouble() - 0.5) * 2 * range, z = getZ() + (random.nextDouble() - 0.5) * 2 * range;
            if (randomTeleport(x, getY() + random.nextInt(4), z, true, s -> false)) {
                playSound(SoundEvents.ENDERMAN_TELEPORT, 1.0F, 0.7F);
                return true;
            }
        }
        return false;
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (riftCooldown > 0) riftCooldown--;
        if (cryCooldown > 0) cryCooldown--;
        if (getTarget() != null) forgive(getTarget());
        LivingEntity target = getTarget();
        if (target == null) return;
        if (cryCooldown == 0 && random.nextInt(40) == 0) {
            cryCooldown = 300;
            String line = DialogueBank.get("court").pick("battle", 0, job, null, random, null);
            if (line != null) CitadelLaw.shout(level, this, Component.literal("<" + getName().getString() + "> "
                    + DialogueBank.fill(line, Map.of("player", target.getName().getString(), "name", firstName, "title", title(), "village", settlement().name()))));
        }
        // a Riftguard steps through the rift to stand behind its quarry
        if (rank == Rank.RIFTGUARD && riftCooldown == 0 && distanceToSqr(target) > 25 && distanceToSqr(target) < 1024) {
            riftCooldown = 100;
            Vec3 behind = target.position().subtract(target.getLookAngle().multiply(1, 0, 1).normalize().scale(2.0));
            if (randomTeleport(behind.x, target.getY() + 2, behind.z, true, s -> false)) {
                playSound(SoundEvents.ENDERMAN_TELEPORT, 1.0F, 0.6F);
                lookAt(target, 180.0F, 90.0F);
            }
        }
    }

    @Override
    public void setTarget(@Nullable LivingEntity target) {
        super.setTarget(target);
        if (target != null) stopTalking();
    }

    @Override protected @Nullable SoundEvent getAmbientSound() { return getTarget() != null ? SoundEvents.ENDERMAN_SCREAM : SoundEvents.ENDERMAN_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.ENDERMAN_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.ENDERMAN_DEATH; }
    @Override public float getVoicePitch() { return (rank == Rank.LORD ? 0.45F : 0.6F) + random.nextFloat() * 0.08F; }
    @Override public int getAmbientSoundInterval() { return 240; }

    /** A target the law no longer names (pardoned, or now a guest) is let go, unless it struck first. */
    private void forgive(LivingEntity target) {
        if (target instanceof ServerPlayer p && !CitadelLaw.isOutlaw(p, this) && getLastHurtByMob() != p) setTarget(null);
    }
}
