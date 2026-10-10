package dev.endexpansion.entity;

import dev.endexpansion.EndEntities;
import dev.endexpansion.world.Settlement;
import net.minecraft.core.BlockPos;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowParentGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.TemptGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jspecify.annotations.Nullable;

/**
 * The Chorrin's herd beast: slow, broad, six-legged, with a little chorus grove on its back. Pick
 * the chorus fruit off a grown one with an empty hand (the grove grows back); breed them with
 * popped chorus fruit. Herded in Steads, wild on the outer islands.
 */
public class Groveback extends Animal implements Settler {
    /** Ticks until the grove on its back has fruit again (0 = ripe). */
    private static final EntityDataAccessor<Integer> REGROW = SynchedEntityData.defineId(Groveback.class, EntityDataSerializers.INT);
    public static final int REGROW_TICKS = 4800;

    private @Nullable Settlement settlement;

    public Groveback(EntityType<? extends Groveback> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder attributes() {
        return createAnimalAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.MOVEMENT_SPEED, 0.17)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    /** End stone underfoot. */
    public static boolean checkSpawnRules(EntityType<Groveback> type, LevelAccessor level, EntitySpawnReason reason, BlockPos pos, RandomSource random) {
        return level.getBlockState(pos.below()).is(Blocks.END_STONE);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(REGROW, 0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new PanicGoal(this, 1.6));
        goalSelector.addGoal(2, new BreedGoal(this, 1.0));
        goalSelector.addGoal(3, new TemptGoal(this, 1.2, this::isFood, false));
        goalSelector.addGoal(4, new FollowParentGoal(this, 1.1));
        goalSelector.addGoal(5, new MoveTowardsRestrictionGoal(this, 1.0));
        goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, 1.0));
        goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 6.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
    }

    @Override
    public Settlement settlement() {
        if (settlement == null) settlement = Settlement.wild("chorrin", blockPosition(), random);
        return settlement;
    }

    /** A Stead's herd stays in its pen. */
    @Override
    public void settle(Settlement settlement, String job, BlockPos home, @Nullable BlockPos work) {
        this.settlement = settlement;
        setHomeTo(home, 5);
        setPersistenceRequired();
    }

    /** 0 just picked, 1 ripe: how far the grove has grown back (the model scales it). */
    public float grove() {
        return 1.0F - entityData.get(REGROW) / (float) REGROW_TICKS;
    }

    public boolean isRipe() {
        return entityData.get(REGROW) == 0 && !isBaby();
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack held = player.getItemInHand(hand);
        if (held.isEmpty() && isRipe()) {
            if (level() instanceof ServerLevel server) {
                int fruit = 2 + random.nextInt(3);
                spawnAtLocation(server, new ItemStack(Items.CHORUS_FRUIT, fruit), 1.6F);
                if (random.nextInt(8) == 0) spawnAtLocation(server, new ItemStack(Items.CHORUS_FLOWER), 1.6F);
                entityData.set(REGROW, REGROW_TICKS);
                level().playSound(null, this, SoundEvents.CAVE_VINES_PICK_BERRIES, SoundSource.NEUTRAL, 1.0F, 0.8F);
            }
            return InteractionResult.SUCCESS;
        }
        return super.mobInteract(player, hand);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide() && entityData.get(REGROW) > 0) entityData.set(REGROW, entityData.get(REGROW) - 1);
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(Items.POPPED_CHORUS_FRUIT);
    }

    @Override
    public @Nullable AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        Groveback calf = EndEntities.GROVEBACK.create(level, EntitySpawnReason.BREEDING);
        if (calf != null && settlement != null) {
            calf.settlement = settlement;
            if (hasHome()) calf.setHomeTo(getHomePosition(), getHomeRadius());
        }
        return calf;
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        output.putInt("Regrow", entityData.get(REGROW));
        if (settlement != null) {
            output.putString("VillageKind", settlement.kind());
            output.store("VillageCenter", BlockPos.CODEC, settlement.center());
            output.putString("VillageName", settlement.name());
        }
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        entityData.set(REGROW, input.getIntOr("Regrow", 0));
        settlement = Settlement.read(input.getStringOr("VillageKind", ""), input.read("VillageCenter", BlockPos.CODEC).orElse(null),
                input.getStringOr("VillageName", ""));
    }

    @Override
    public boolean removeWhenFarAway(double distSqr) {
        return false;
    }

    @Override protected @Nullable SoundEvent getAmbientSound() { return SoundEvents.SNIFFER_IDLE; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.SNIFFER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.SNIFFER_DEATH; }
    @Override protected void playStepSound(BlockPos pos, BlockState state) { playSound(SoundEvents.SNIFFER_STEP, 0.4F, 0.8F); }
    @Override public float getVoicePitch() { return (isBaby() ? 1.3F : 0.75F) + random.nextFloat() * 0.1F; }
    @Override public int getAmbientSoundInterval() { return 240; }
}
