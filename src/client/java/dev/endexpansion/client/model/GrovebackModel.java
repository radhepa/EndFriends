package dev.endexpansion.client.model;

import dev.endexpansion.client.render.EndRenderState;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/**
 * Six legs in a slow tripod gait (front and back of one side with the middle of the other), a
 * grazing head that dips now and then, a swaying tail, and the grove on its back: picked bare it
 * shrinks to a stub and grows back.
 */
public class GrovebackModel extends EndModel {
    private final ModelPart head, tail, grove;
    private final ModelPart[] right = new ModelPart[3], left = new ModelPart[3];

    public GrovebackModel(ModelPart root) {
        super(root, "groveback");
        head = part("head");
        tail = part("tail");
        grove = part("grove");
        for (int i = 0; i < 3; i++) {
            right[i] = part("right_leg_" + i);
            left[i] = part("left_leg_" + i);
        }
    }

    @Override
    public void setupAnim(EndRenderState s) {
        super.setupAnim(s);
        float t = s.ageInTicks;
        look(head, s, 0.6F);
        float step = walk(s, 0.5F) * 0.8F;
        for (int i = 0; i < 3; i++) {
            float sign = i % 2 == 0 ? 1.0F : -1.0F;
            right[i].xRot += step * sign;
            left[i].xRot -= step * sign;
        }
        // grazing: now and then the head dips to the ground for a while
        float graze = Math.max(0.0F, Mth.sin(t * 0.02F) - 0.7F) / 0.3F;
        if (s.walkAnimationSpeed < 0.1F) head.xRot += graze * 0.9F;
        tail.yRot += Mth.sin(t * 0.08F) * 0.25F;
        float g = 0.25F + 0.75F * s.grove;
        grove.xScale = g;
        grove.yScale = g;
        grove.zScale = g;
    }
}
