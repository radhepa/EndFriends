package dev.endexpansion.client.model;

import dev.endexpansion.client.render.EndRenderState;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/**
 * The Court's hound moves like a Minecraft wolf (it is built on the wolf's boxes): a diagonal trot,
 * the wolf's sitting pose, a wagging tail (raised when angry), and its shards bobbing over its back.
 */
public class VoidhoundModel extends EndModel {
    private final ModelPart body, upperBody, head, rightHind, leftHind, rightFront, leftFront, tail, shards;

    public VoidhoundModel(ModelPart root, String id) {
        super(root, id);
        body = part("body");
        upperBody = part("upper_body");
        head = part("head");
        rightHind = part("right_hind_leg");
        leftHind = part("left_hind_leg");
        rightFront = part("right_front_leg");
        leftFront = part("left_front_leg");
        tail = part("tail");
        shards = part("shards");
    }

    @Override
    public void setupAnim(EndRenderState s) {
        super.setupAnim(s);
        float t = s.ageInTicks;
        look(head, s, 1.0F);
        shards.y -= Mth.sin(t * 0.1F) * 0.6F;
        shards.yRot += t * 0.02F;
        if (s.sitting) {
            // the wolf's sitting pose
            upperBody.xRot -= 0.2F;
            upperBody.y += 1.0F;
            body.xRot -= 0.8F;
            body.y += 3.0F;
            body.z -= 1.5F;
            tail.y += 6.0F;
            tail.z -= 2.0F;
            rightHind.xRot = -1.57F;
            leftHind.xRot = -1.57F;
            rightHind.y += 5.0F;
            leftHind.y += 5.0F;
            rightHind.z -= 3.0F;
            leftHind.z -= 3.0F;
            rightFront.xRot = -0.15F;
            leftFront.xRot = -0.15F;
            rightFront.y += 1.0F;
            leftFront.y += 1.0F;
            return;
        }
        float step = walk(s, 0.6662F) * 1.4F;
        rightHind.xRot += step;
        leftFront.xRot += step;
        leftHind.xRot -= step;
        rightFront.xRot -= step;
        tail.yRot += Mth.cos(s.walkAnimationPos * 0.6662F) * 1.4F * s.walkAnimationSpeed + Mth.sin(t * 0.3F) * 0.15F;
        if (s.aggressive) tail.xRot -= 0.35F;
    }
}
