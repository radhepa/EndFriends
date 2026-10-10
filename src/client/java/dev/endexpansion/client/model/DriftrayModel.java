package dev.endexpansion.client.model;

import dev.endexpansion.client.render.EndRenderState;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/**
 * Slow, rippling wingbeats (the tips trail the wings), deeper and faster with a rider in flight,
 * and a tail that sways behind.
 */
public class DriftrayModel extends EndModel {
    private final ModelPart body, rightWing, leftWing, rightTip, leftTip, tail;

    public DriftrayModel(ModelPart root) {
        super(root, "driftray");
        body = part("body");
        rightWing = part("right_wing");
        leftWing = part("left_wing");
        rightTip = part("right_tip");
        leftTip = part("left_tip");
        tail = part("tail");
    }

    @Override
    public void setupAnim(EndRenderState s) {
        super.setupAnim(s);
        float t = s.ageInTicks;
        float rate = s.flying ? 0.32F : 0.14F, depth = s.flying ? 0.55F : 0.3F;
        float beat = Mth.sin(t * rate);
        float trail = Mth.sin(t * rate - 0.9F);
        rightWing.zRot += beat * depth;
        leftWing.zRot -= beat * depth;
        rightTip.zRot += trail * depth * 0.8F;
        leftTip.zRot -= trail * depth * 0.8F;
        body.y -= beat * (s.flying ? 0.8F : 0.4F);
        body.xRot += s.flying ? -0.08F : 0.0F;
        tail.yRot += Mth.sin(t * 0.1F) * 0.2F;
        tail.xRot += Mth.sin(t * rate + 0.5F) * 0.08F;
    }
}
