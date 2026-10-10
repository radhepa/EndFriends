package dev.endexpansion.client.render;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.endexpansion.client.model.EndModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;

/** A thrall's block of the Court's stone, held out in front like an Enderman's. */
public class CarriedStoneLayer extends RenderLayer<EndRenderState, EndModel> {
    public CarriedStoneLayer(RenderLayerParent<EndRenderState, EndModel> renderer) {
        super(renderer);
    }

    @Override
    public void submit(PoseStack poseStack, SubmitNodeCollector collector, int light, EndRenderState state, float yRot, float xRot) {
        if (!state.carrying || state.carriedBlock.isEmpty()) return;
        poseStack.pushPose();
        poseStack.translate(0.0F, 0.5F, -0.75F);
        poseStack.rotateDegrees(Axis.XP, 20.0F);
        poseStack.rotateDegrees(Axis.YP, 45.0F);
        poseStack.translate(0.25F, 0.1875F, 0.25F);
        poseStack.scale(-0.5F, -0.5F, 0.5F);
        poseStack.rotateDegrees(Axis.YP, 90.0F);
        state.carriedBlock.submit(poseStack, collector, light, OverlayTexture.NO_OVERLAY, state.outlineColor);
        poseStack.popPose();
    }
}
