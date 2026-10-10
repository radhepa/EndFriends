package dev.endexpansion.entity;

import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.world.Settlement;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowOwnerGoal;
import net.minecraft.world.entity.ai.goal.LeapAtTargetGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.SitWhenOrderedToGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.goal.target.OwnerHurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.OwnerHurtTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * The Court's hound: a void-black wolf with an obsidian collar and shards floating over its back.
 * In a Citadel it runs with the Riftguards and reaches outlaws first, hopping through short rifts.
 * A Lord gives a pup (purpur collar) to a guest in high Favor: it grows up and behaves like a tamed
 * wolf (sit, follow, fight for its owner, meat to heal).
 */
public class Voidhound extends TamableAnimal implements Settler {
    private @Nullable Settlement settlement;
    private int hopCooldown;

    public Voidhound(EntityType<? extends Voidhound> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder attributes() {
        return createAnimalAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.MOVEMENT_SPEED, 0.33)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(1, new FloatGoal(this));
        goalSelector.addGoal(2, new SitWhenOrderedToGoal(this));
        goalSelector.addGoal(3, new LeapAtTargetGoal(this, 0.4F));
        goalSelector.addGoal(4, new MeleeAttackGoal(this, 1.2, true));
        goalSelector.addGoal(5, new FollowOwnerGoal(this, 1.0, 10.0F, 2.0F));
        goalSelector.addGoal(6, new MoveTowardsRestrictionGoal(this, 0.8));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.8));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new OwnerHurtByTargetGoal(this));
        targetSelector.addGoal(2, new OwnerHurtTargetGoal(this));
        targetSelector.addGoal(3, new HurtByTargetGoal(this).setAlertOthers(Voidhound.class));
        targetSelector.addGoal(4, new NearestAttackableTargetGoal<>(this, Player.class, false,
                (target, level) -> !isTame() && CitadelLaw.isOutlaw(target, this)));
    }

    // -- the Court's hound ------------------------------------------------------------------------

    @Override
    public Settlement settlement() {
        if (settlement == null) settlement = Settlement.wild("court", blockPosition(), random);
        return settlement;
    }

    @Override
    public void settle(Settlement settlement, String job, BlockPos home, @Nullable BlockPos work) {
        this.settlement = settlement;
        setHomeTo(home, 12);
    }

    /** A pup from the Lord: tamed to its new owner, small, free to follow them anywhere. */
    public void makePup(ServerPlayer owner) {
        setAge(-24000);
        tame(owner);
        clearHome();
        setPersistenceRequired();
        setHealth(getMaxHealth());
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ItemTags.WOLF_FOOD);
    }

    /** Pups come only from the Court. */
    @Override
    public @Nullable AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        return null;
    }

    @Override
    public boolean canFallInLove() {
        return false;
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!isTame() || !isOwnedBy(player)) return InteractionResult.PASS;
        if (isFood(stack) && getHealth() < getMaxHealth()) {
            if (!level().isClientSide()) {
                usePlayerItem(player, hand, stack);
                heal(4.0F);
                if (isBaby()) ageUp(60);
                playSound(SoundEvents.GENERIC_EAT.value(), 0.8F, 1.0F);
            }
            return InteractionResult.SUCCESS;
        }
        if (!level().isClientSide()) {
            setOrderedToSit(!isOrderedToSit());
            jumping = false;
            getNavigation().stop();
            setTarget(null);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public boolean wantsToAttack(LivingEntity target, LivingEntity owner) {
        if (target instanceof TamableAnimal t && t.isTame() && t.getOwner() == owner) return false;
        return !(target instanceof Player p && owner instanceof Player o && !o.canHarmPlayer(p));
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        if (!isTame() && source.getEntity() instanceof ServerPlayer player) CitadelLaw.strike(player, this);
        if (!level.isClientSide()) setOrderedToSit(false);
        return super.hurtServer(level, source, damage);
    }

    /** Hops through a short rift toward whatever it chases. */
    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (hopCooldown > 0) hopCooldown--;
        if (getTarget() != null && !isTame()) forgive(getTarget());
        LivingEntity target = getTarget();
        if (target != null && hopCooldown == 0 && distanceToSqr(target) > 36 && distanceToSqr(target) < 900) {
            hopCooldown = 60;
            Vec3 toward = position().add(target.position().subtract(position()).normalize().scale(4.0 + random.nextDouble() * 2));
            if (randomTeleport(toward.x, toward.y + 2, toward.z, true, s -> false)) playSound(SoundEvents.ENDERMAN_TELEPORT, 0.6F, 1.4F);
        }
    }

    @Override
    public boolean removeWhenFarAway(double distSqr) {
        return false;
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        if (settlement != null) {
            output.putString("VillageKind", settlement.kind());
            output.store("VillageCenter", BlockPos.CODEC, settlement.center());
            output.putString("VillageName", settlement.name());
        }
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        settlement = Settlement.read(input.getStringOr("VillageKind", ""), input.read("VillageCenter", BlockPos.CODEC).orElse(null),
                input.getStringOr("VillageName", ""));
    }

    // -- sounds: a wolf's, deeper ------------------------------------------------------------------

    private static SoundEvent wolf(String sound) {
        return BuiltInRegistries.SOUND_EVENT.getValue(Identifier.withDefaultNamespace("entity.wolf." + sound));
    }

    @Override protected @Nullable SoundEvent getAmbientSound() {
        return isBaby() ? SoundEvents.WOLF_AMBIENT_BABY.value() : getTarget() != null ? wolf("growl") : wolf("ambient");
    }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return isBaby() ? SoundEvents.WOLF_HURT_BABY.value() : wolf("hurt"); }
    @Override protected SoundEvent getDeathSound() { return isBaby() ? SoundEvents.WOLF_DEATH_BABY.value() : wolf("death"); }
    @Override public float getVoicePitch() { return (isBaby() ? 1.2F : 0.7F) + random.nextFloat() * 0.1F; }

    /** A target the law no longer names (pardoned, or now a guest) is let go, unless it struck first. */
    private void forgive(LivingEntity target) {
        if (target instanceof ServerPlayer p && !CitadelLaw.isOutlaw(p, this) && getLastHurtByMob() != p) setTarget(null);
    }
}
