package dev.endexpansion.client.model;

import dev.endexpansion.client.render.EndRenderState;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;
import org.jspecify.annotations.Nullable;

/** Base for the mod's models: parts by name from the geometry file, and a head that follows the gaze. */
public abstract class EndModel extends EntityModel<EndRenderState> {
    protected final String id;

    protected EndModel(ModelPart root, String id) {
        super(root);
        this.id = id;
    }

    public String id() {
        return id;
    }

    protected ModelPart part(String name) {
        return Geometry.part(root(), id, name);
    }

    protected @Nullable ModelPart optional(String name) {
        return Geometry.optional(root(), id, name);
    }

    /** Turn a head toward where the mob is looking (degrees from the render state). */
    protected static void look(ModelPart head, EndRenderState s, float weight) {
        head.yRot += s.yRot * Mth.DEG_TO_RAD * weight;
        head.xRot += s.xRot * Mth.DEG_TO_RAD * weight;
    }

    protected static float walk(EndRenderState s, float rate) {
        return Mth.cos(s.walkAnimationPos * rate) * s.walkAnimationSpeed;
    }
}
