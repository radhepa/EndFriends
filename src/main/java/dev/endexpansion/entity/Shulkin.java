package dev.endexpansion.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import org.jspecify.annotations.Nullable;

/**
 * Shell-folk of the purpur Spires. Hurt or frightened, a Shulkin slams its lid shut and takes far
 * less damage until it dares to peek out again; it sleeps closed too. Each is named for the lamp lit
 * when their lid first opened. Children have soft pale shells and pop open at everything.
 */
public class Shulkin extends Resident {
    private static final String[] LAMPS = {"First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth",
            "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Last", "Old", "Low"};
    /** How long the lid stays shut after a blow, and how much a closed shell lets through. */
    private static final int CLOSED_TICKS = 60;
    private static final float CLOSED_DAMAGE = 0.25F;

    private final boolean child;
    private int closed;

    public Shulkin(EntityType<? extends Shulkin> type, Level level, boolean child) {
        super(type, level);
        this.child = child;
    }

    @Override public String people() { return "shulkin"; }
    @Override public boolean isChild() { return child; }
    @Override protected String defaultJob() { return child ? "" : "keeper"; }

    @Override
    public String title() {
        if (child) return "Young Shulkin";
        return switch (job) {
            case "archivist" -> "Archivist";
            case "lamplighter" -> "Lamplighter";
            case "weaver" -> "Weaver";
            case "shellwright" -> "Shellwright";
            case "wayfinder" -> "Wayfinder";
            case "hallkeeper" -> "Hallkeeper";
            case "trader" -> "Trader";
            default -> "Keeper of Shells";
        };
    }

    @Override
    protected String fullName(String first, RandomSource random) {
        return first + " of the " + LAMPS[random.nextInt(LAMPS.length)] + " Lamp";
    }

    /** The lid is shut: after a blow, and all night. */
    public boolean isClosed() {
        return flag(CLOSED);
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        if (closed > 0) damage *= CLOSED_DAMAGE;
        boolean hurt = super.hurtServer(level, source, damage);
        if (hurt && isAlive()) {
            if (closed == 0) playSound(SoundEvents.SHULKER_CLOSE, 1.0F, child ? 1.4F : 1.0F);
            closed = CLOSED_TICKS;
            setFlag(CLOSED, true);
        }
        return hurt;
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (closed > 0 && --closed == 0) playSound(SoundEvents.SHULKER_OPEN, 1.0F, child ? 1.4F : 1.0F);
        setFlag(CLOSED, closed > 0 || isSleeping());
        if (closed > 0) getNavigation().stop();
    }

    @Override protected @Nullable SoundEvent getAmbientSound() { return isSleeping() ? null : SoundEvents.SHULKER_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return closed > 0 ? SoundEvents.SHULKER_HURT_CLOSED : SoundEvents.SHULKER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.SHULKER_DEATH; }
    @Override public float getVoicePitch() { return (child ? 1.5F : 1.05F) + random.nextFloat() * 0.1F; }
    @Override public int getAmbientSoundInterval() { return 300; }
    @Override protected float getSoundVolume() { return 0.7F; }
}
