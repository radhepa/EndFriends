package dev.endexpansion.client.render;

import com.mojang.blaze3d.vertex.PoseStack;
import dev.endexpansion.EndExpansion;
import dev.endexpansion.client.model.EndModel;
import dev.endexpansion.client.model.Geometry;
import java.util.HashMap;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.rendertype.RenderType;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.Mob;
import org.jspecify.annotations.Nullable;

/**
 * Renderer for every mob in the mod: a model baked from its geometry file, drawn at the file's scale,
 * with its texture and (when the art has one) a glowing layer. A mob with a separate young model
 * (the Voidhound pup) switches to it while young.
 */
public class EndRenderer<T extends Mob> extends MobRenderer<T, EndRenderState, EndModel> {
    private final EndModel adult;
    private final @Nullable EndModel young;
    private final BiConsumer<T, EndRenderState> extract;
    private final Map<String, Identifier> textures = new HashMap<>();

    public EndRenderer(EntityRendererProvider.Context context, String id, @Nullable String youngId,
                       BiFunction<ModelPart, String, EndModel> model, float shadow, BiConsumer<T, EndRenderState> extract) {
        super(context, model.apply(context.bakeLayer(Geometry.layer(id)), id), shadow);
        this.adult = this.model;
        this.young = youngId == null ? null : model.apply(context.bakeLayer(Geometry.layer(youngId)), youngId);
        this.extract = extract;
        addLayer(new Glow(this));
    }

    public EndRenderer(EntityRendererProvider.Context context, String id, BiFunction<ModelPart, String, EndModel> model, float shadow,
                       BiConsumer<T, EndRenderState> extract) {
        this(context, id, null, model, shadow, extract);
    }

    /** Also draw a carried block (thralls). */
    public EndRenderer<T> carrying() {
        addLayer(new CarriedStoneLayer(this));
        return this;
    }

    private EndModel modelFor(EndRenderState state) {
        return state.isBaby && young != null ? young : adult;
    }

    @Override
    public void submit(EndRenderState state, PoseStack poseStack, SubmitNodeCollector collector, CameraRenderState camera) {
        this.model = modelFor(state);
        super.submit(state, poseStack, collector, camera);
    }

    @Override
    public Identifier getTextureLocation(EndRenderState state) {
        return texture(modelFor(state).id());
    }

    private Identifier texture(String id) {
        return textures.computeIfAbsent(id, k -> EndExpansion.id("textures/entity/" + k + ".png"));
    }

    /** The geometry's own scale; young animals without a model of their own are also shrunk. */
    @Override
    protected void scale(EndRenderState state, PoseStack poseStack) {
        EndModel m = modelFor(state);
        float s = Geometry.scale(m.id()) * (state.isBaby && young == null ? state.ageScale : 1.0F);
        if (s != 1.0F) poseStack.scale(s, s, s);
    }

    @Override
    public EndRenderState createRenderState() {
        return new EndRenderState();
    }

    @Override
    public void extractRenderState(T entity, EndRenderState state, float partialTicks) {
        super.extractRenderState(entity, state, partialTicks);
        state.aggressive = entity.isAggressive();
        state.swing = entity.getSwingAnimation(partialTicks);
        extract.accept(entity, state);
    }

    /** Draws {@code <id>_glow.png} at full brightness when the art has one (eyes, gaps, rods). */
    private static final class Glow extends RenderLayer<EndRenderState, EndModel> {
        private final Map<String, java.util.Optional<RenderType>> types = new HashMap<>();

        Glow(EndRenderer<?> renderer) {
            super(renderer);
        }

        @Override
        public void submit(PoseStack poseStack, SubmitNodeCollector collector, int light, EndRenderState state, float yRot, float xRot) {
            EndModel model = getParentModel();
            RenderType type = types.computeIfAbsent(model.id(), id -> {
                String path = "textures/entity/" + id + "_glow.png";
                return Glow.class.getResource("/assets/" + EndExpansion.MOD_ID + "/" + path) == null
                        ? java.util.Optional.empty() : java.util.Optional.of(RenderTypes.eyes(EndExpansion.id(path)));
            }).orElse(null);
            if (type != null) collector.order(1).submitModel(model, state, poseStack, type, light, OverlayTexture.NO_OVERLAY, state.outlineColor);
        }
    }
}
