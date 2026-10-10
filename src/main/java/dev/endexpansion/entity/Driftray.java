package dev.endexpansion.entity;

import dev.endexpansion.world.Settlement;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RunAroundLikeCrazyGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * A manta that glides on the void currents. Wild ones drift a couple of blocks over the islands
 * (never sinking into the void). Tame one by feeding it chorus flowers (or riding it until it
 * accepts you), saddle it, and it carries you across the gaps: jump to rise, hold forward to fly
 * where you look, let go to glide slowly down. It never falls hard, and neither do you.
 */
public class Driftray extends AbstractHorse implements Settler {
    /** Flying with a rider (the server's view, synced). */
    private static final EntityDataAccessor<Boolean> FLYING = SynchedEntityData.defineId(Driftray.class, EntityDataSerializers.BOOLEAN);
    private static final double FLY_SPEED = 0.6, MAX_CLIMB = 0.3, MAX_DIVE = -0.6, HOVER_SINK = -0.02, GLIDE_FALL = -0.06;
    private static final double TURN = 0.05, RISE = 0.07, SINK = 0.12;
    /** Wild drifting: height over the ground it keeps, and its speed. */
    private static final double DRIFT_HEIGHT = 2.5, DRIFT_SPEED = 0.07;

    private @Nullable Settlement settlement;
    private boolean localFlight;
    private float heading;
    private int headingTicks;

    public Driftray(EntityType<? extends Driftray> type, Level level) {
        super(type, level);
        this.heading = random.nextFloat() * 360.0F;
    }

    public static AttributeSupplier.Builder attributes() {
        return AbstractHorse.createBaseHorseAttributes()
                .add(Attributes.MAX_HEALTH, 24.0)
                .add(Attributes.MOVEMENT_SPEED, 0.2)
                .add(Attributes.JUMP_STRENGTH, 0.6);
    }

    /** End stone underfoot: the outer islands. */
    public static boolean checkSpawnRules(EntityType<Driftray> type, LevelAccessor level, EntitySpawnReason reason, BlockPos pos, RandomSource random) {
        return level.getBlockState(pos.below()).is(Blocks.END_STONE);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(FLYING, false);
    }

    /** No grazing or wandering on foot: it drifts (see {@link #travel}). Riding an untamed one still tames it, horse-fashion. */
    @Override
    protected void registerGoals() {
        goalSelector.addGoal(1, new RunAroundLikeCrazyGoal(this, 1.2));
        goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(7, new RandomLookAroundGoal(this));
    }

    @Override
    protected void randomizeAttributes(RandomSource random) {
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(24.0);
    }

    // -- settlement --------------------------------------------------------------------------------

    @Override
    public Settlement settlement() {
        if (settlement == null) settlement = Settlement.wild("shulkin", blockPosition(), random);
        return settlement;
    }

    /** A Spire's rays drift round their roost. */
    @Override
    public void settle(Settlement settlement, String job, BlockPos home, @Nullable BlockPos work) {
        this.settlement = settlement;
        setHomeTo(home, 12);
        setPersistenceRequired();
    }

    // -- flight ------------------------------------------------------------------------------------

    /** Wings spread in flight with a rider; true on every client. */
    public boolean isFlying() {
        return entityData.get(FLYING) || localFlight;
    }

    private boolean canFly() {
        return !isBaby() && isSaddled() && getControllingPassenger() instanceof Player;
    }

    private boolean aloft() {
        return !onGround() && !isInWater();
    }

    @Override
    public void onPlayerJump(int amount) {
        if (canFly() && !onGround()) {
            localFlight = true;
            Vec3 v = getDeltaMovement();
            setDeltaMovement(v.x, Math.max(v.y, 0.0) + 0.35 + 0.25 * getPlayerJumpPendingScale(Math.max(amount, 0)), v.z);
            return;
        }
        super.onPlayerJump(amount);
    }

    @Override
    protected void executeRidersJump(float amount, Vec3 input) {
        if (canFly()) {
            Vec3 v = getDeltaMovement();
            setDeltaMovement(v.x, 0.4 + 0.45 * amount, v.z);
            localFlight = true;
            return;
        }
        super.executeRidersJump(amount, input);
    }

    @Override
    public void handleStartJump(int jumpScale) {
        if (canFly()) {
            entityData.set(FLYING, true);
            return;
        }
        super.handleStartJump(jumpScale);
    }

    @Override
    public void travel(Vec3 input) {
        if (getControllingPassenger() == null && !isVehicle()) {
            drift();
            return;
        }
        boolean powered = canFly() && aloft() && (localFlight || entityData.get(FLYING));
        if (isNoGravity() != powered) setNoGravity(powered);
        if (powered) {
            fly(input);
            return;
        }
        super.travel(input);
        Vec3 v = getDeltaMovement();
        if (aloft() && v.y < GLIDE_FALL) setDeltaMovement(v.x, GLIDE_FALL, v.z);   // it glides, never falls
    }

    /** With a rider: velocity eases toward where they look (forward held), or a slow sinking hover. */
    private void fly(Vec3 input) {
        LivingEntity rider = getControllingPassenger();
        float pitch = rider != null ? rider.getXRot() : 0.0F;
        float yaw = getYRot();
        double sin = Mth.sin(yaw * Mth.DEG_TO_RAD), cos = Mth.cos(yaw * Mth.DEG_TO_RAD);
        Vec3 target;
        if (input.z > 0) {
            Vec3 look = Vec3.directionFromRotation(pitch, yaw).scale(FLY_SPEED * input.z);
            target = new Vec3(look.x, Mth.clamp(look.y, MAX_DIVE, MAX_CLIMB), look.z);
        } else {
            target = new Vec3(-sin * input.z * 0.5, HOVER_SINK, cos * input.z * 0.5);
        }
        target = target.add(cos * input.x * 0.5, 0.0, sin * input.x * 0.5);
        Vec3 v = getDeltaMovement();
        double vy = v.y + (target.y - v.y) * (v.y > target.y ? SINK : RISE);
        v = new Vec3(v.x + (target.x - v.x) * TURN, vy, v.z + (target.z - v.z) * TURN);
        setDeltaMovement(v);
        move(MoverType.SELF, v);
        if (onGround() || isInWater()) localFlight = false;
    }

    /** Without a rider: hang a couple of blocks over the ground and drift, turning now and then. */
    private void drift() {
        if (!isNoGravity()) setNoGravity(true);
        boolean tameAndStill = isTamed() || isLeashed();
        if (--headingTicks <= 0) {
            headingTicks = 60 + random.nextInt(120);
            heading += (random.nextFloat() - 0.5F) * 120.0F;
            if (hasHome() && !isWithinHome()) {
                Vec3 to = Vec3.atCenterOf(getHomePosition()).subtract(position());
                heading = (float) (Mth.atan2(to.z, to.x) * Mth.RAD_TO_DEG) - 90.0F;
            }
        }
        double ground = groundBelow();
        double wantY = Double.isNaN(ground) ? getY() : ground + DRIFT_HEIGHT + Mth.sin(tickCount * 0.05F) * 0.4;
        double speed = tameAndStill ? 0.0 : DRIFT_SPEED;
        double rad = heading * Mth.DEG_TO_RAD;
        Vec3 want = new Vec3(-Math.sin(rad) * speed, Mth.clamp((wantY - getY()) * 0.05, -0.08, 0.08), Math.cos(rad) * speed);
        Vec3 v = getDeltaMovement();
        v = v.add(want.subtract(v).scale(0.1));
        // never out over the void: turn back toward land
        if (Double.isNaN(ground) && !tameAndStill) heading += 6.0F;
        setDeltaMovement(v);
        move(MoverType.SELF, v);
        if (v.horizontalDistanceSqr() > 1.0E-4) {
            float face = (float) (Mth.atan2(v.z, v.x) * Mth.RAD_TO_DEG) - 90.0F;
            setYRot(Mth.rotLerp(0.1F, getYRot(), face));
            yBodyRot = getYRot();
        }
        if (horizontalCollision) heading += 90.0F;
    }

    /** The top of the ground up to 24 blocks below, or NaN over the void. */
    private double groundBelow() {
        BlockPos.MutableBlockPos p = blockPosition().mutable();
        for (int i = 0; i < 24; i++) {
            if (!level().getBlockState(p).getCollisionShape(level(), p).isEmpty()) return p.getY() + 1.0;
            p.move(0, -1, 0);
        }
        return Double.NaN;
    }

    @Override
    public void tick() {
        super.tick();
        if (!aloft() || !isVehicle()) localFlight = false;
        resetFallDistance();
        for (Entity rider : getPassengers()) rider.resetFallDistance();
        if (!level().isClientSide()) {
            boolean flying = canFly() && aloft();
            if (flying != entityData.get(FLYING)) entityData.set(FLYING, flying);
            if (isVehicle() && !canFly() && isNoGravity()) setNoGravity(false);
        } else if (random.nextInt(6) == 0) {
            level().addParticle(ParticleTypes.PORTAL, getRandomX(1.2), getY() + 0.2, getRandomZ(1.2), 0, -0.05, 0);
        }
    }

    @Override public boolean isFlyingVehicle() { return isFlying(); }

    @Override
    public boolean causeFallDamage(double fallDistance, float damageModifier, DamageSource damageSource) {
        return false;
    }

    // -- taming, food -----------------------------------------------------------------------------

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(Items.CHORUS_FLOWER) || stack.is(Items.CHORUS_FRUIT) || stack.is(Items.POPPED_CHORUS_FRUIT);
    }

    /** Chorus flowers win it over; chorus fruit (raw or popped) heals it. */
    @Override
    protected boolean handleEating(Player player, ItemStack stack) {
        boolean used = false;
        float heal = stack.is(Items.CHORUS_FLOWER) ? 4.0F : stack.is(Items.POPPED_CHORUS_FRUIT) ? 3.0F : 2.0F;
        if (getHealth() < getMaxHealth()) {
            heal(heal);
            used = true;
        }
        if (stack.is(Items.CHORUS_FLOWER) && !isTamed() && getTemper() < getMaxTemper()) {
            if (!level().isClientSide()) modifyTemper(20);
            used = true;
        }
        if (used) {
            playSound(SoundEvents.GENERIC_EAT.value(), 0.8F, 1.2F);
            gameEvent(GameEvent.EAT);
            if (!level().isClientSide() && !isTamed() && getTemper() >= getMaxTemper() && level() instanceof ServerLevel) tameWithName(player);
        }
        return used;
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        boolean openInventory = isTamed() && player.isSecondaryUseActive();
        if (!isVehicle() && !openInventory) {
            ItemStack stack = player.getItemInHand(hand);
            if (!stack.isEmpty() && isFood(stack)) return fedFood(player, stack);
        }
        return super.mobInteract(player, hand);
    }

    @Override protected boolean canPerformRearing() { return false; }
    @Override public boolean canEatGrass() { return false; }
    @Override public boolean canUseSlot(EquipmentSlot slot) { return slot != EquipmentSlot.BODY && super.canUseSlot(slot); }
    @Override public boolean canMate(Animal partner) { return false; }
    @Override public @Nullable AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) { return null; }

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

    @Override
    public boolean removeWhenFarAway(double distSqr) {
        return false;
    }

    // -- sounds ------------------------------------------------------------------------------------
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.ALLAY_AMBIENT_WITHOUT_ITEM; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.PHANTOM_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.PHANTOM_DEATH; }
    @Override protected @Nullable SoundEvent getEatingSound() { return SoundEvents.GENERIC_EAT.value(); }
    @Override protected @Nullable SoundEvent getAngrySound() { return SoundEvents.PHANTOM_AMBIENT; }
    @Override protected void playStepSound(BlockPos pos, net.minecraft.world.level.block.state.BlockState state) {}
    @Override protected float getSoundVolume() { return 0.5F; }
    @Override public float getVoicePitch() { return 0.6F + random.nextFloat() * 0.1F; }
    @Override public int getAmbientSoundInterval() { return 300; }
}
