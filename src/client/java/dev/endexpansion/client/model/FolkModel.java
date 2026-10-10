package dev.endexpansion.client.model;

import dev.endexpansion.client.render.EndRenderState;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;
import org.jspecify.annotations.Nullable;

/**
 * Every person of the End: Shulkin and Chorrin (and their children), the Endarchs and the thralls.
 * They share a body plan (head, two arms with optional forearms, two legs with optional shins) and
 * these poses: walking, looking, talking (a Shulkin's lid lifts, a Chorrin's crown sways as it hums),
 * working at their trade, a Shulkin shut in its shell, asleep (Shulkin curled shut, everyone else
 * sitting), carrying a block (thralls), and striking.
 */
public class FolkModel extends EndModel {
    /** How far the Shulkin lid sits above the collar in the model: closing it lowers it by this. */
    private static final float LID_GAP = 4.0F;

    private final ModelPart body, head, rightArm, leftArm, rightLeg, leftLeg;
    private final @Nullable ModelPart lid, crown, rightForearm, leftForearm, rightShin, leftShin, cape;
    private final float legLength;

    public FolkModel(ModelPart root, String id) {
        super(root, id);
        body = part("body");
        head = part("head");
        rightArm = part("right_arm");
        leftArm = part("left_arm");
        rightLeg = part("right_leg");
        leftLeg = part("left_leg");
        lid = optional("lid");
        crown = optional("crown");
        rightForearm = optional("right_forearm");
        leftForearm = optional("left_forearm");
        rightShin = optional("right_shin");
        leftShin = optional("left_shin");
        ModelPart c = optional("cape");
        cape = c != null ? c : optional("mantle");
        legLength = 24.0F - rightLeg.y;
    }

    @Override
    public void setupAnim(EndRenderState s) {
        super.setupAnim(s);
        float t = s.ageInTicks;
        boolean shulkin = lid != null;

        if (s.sleeping) {
            sleep(s, shulkin, t);
            return;
        }

        look(head, s, s.closed ? 0.2F : 1.0F);
        // walking: long arms swing less than legs
        float step = walk(s, 0.6662F);
        rightLeg.xRot += step * 1.1F;
        leftLeg.xRot -= step * 1.1F;
        if (rightShin != null) rightShin.xRot += Math.max(0.0F, -step) * 0.9F;
        if (leftShin != null) leftShin.xRot += Math.max(0.0F, step) * 0.9F;
        rightArm.xRot -= step * 0.55F;
        leftArm.xRot += step * 0.55F;
        // breathing sway
        float sway = Mth.sin(t * 0.067F) * 0.04F;
        rightArm.zRot += 0.04F + sway;
        leftArm.zRot -= 0.04F + sway;
        if (cape != null) cape.xRot += s.walkAnimationSpeed * 0.35F + Mth.sin(t * 0.08F) * 0.02F;
        // a Shulkin glides a pixel off the ground, bobbing gently
        if (shulkin) body.y -= Mth.sin(t * 0.1F) * 0.3F;

        if (lid != null) {
            if (s.closed) {
                lid.y += LID_GAP;
                head.xRot += 0.25F;
            } else if (s.talking) {
                lid.y -= 1.0F + Mth.sin(t * 0.45F) * 0.8F;
                lid.xRot -= 0.12F;
            }
        }
        if (crown != null && s.talking) {
            crown.zRot += Mth.sin(t * 0.5F) * 0.06F;     // the hum shakes it
            head.xRot += Mth.sin(t * 0.25F) * 0.04F;
        }

        if (s.carrying) {
            rightArm.xRot = -0.75F;
            leftArm.xRot = -0.75F;
            rightArm.zRot = 0.05F;
            leftArm.zRot = -0.05F;
        } else if (s.working && !s.talking) {
            // busy hands at their trade
            rightArm.xRot -= 0.8F + Mth.sin(t * 0.25F) * 0.25F;
            leftArm.xRot -= 0.6F + Mth.cos(t * 0.2F) * 0.2F;
            if (rightForearm != null) rightForearm.xRot -= 0.3F + Mth.sin(t * 0.25F) * 0.2F;
            head.xRot += 0.3F;
        } else if (s.talking) {
            // a gesture now and then
            float g = Math.max(0.0F, Mth.sin(t * 0.09F));
            rightArm.xRot -= g * 0.5F;
            if (rightForearm != null) rightForearm.xRot -= g * 0.4F;
        }

        if (s.aggressive && !s.carrying) {
            rightArm.xRot -= 0.5F;
            leftArm.xRot -= 0.3F;
        }
        if (s.swing > 0.0F) {
            float k = Mth.sin(s.swing * Mth.PI);
            rightArm.xRot -= k * 2.0F;
            rightArm.zRot -= k * 0.3F;
            body.yRot -= k * 0.25F;
            if (rightForearm != null) rightForearm.xRot -= k * 0.4F;
        }
    }

    /** Shulkin curl up shut; everyone else sits with their legs out. */
    private void sleep(EndRenderState s, boolean shulkin, float t) {
        if (shulkin) {
            lid.y += LID_GAP;
            head.xRot += 0.45F;
            rightArm.xRot -= 0.9F;
            leftArm.xRot -= 0.9F;
            rightArm.zRot -= 0.35F;
            leftArm.zRot += 0.35F;
            if (rightForearm != null) rightForearm.xRot -= 0.8F;
            if (leftForearm != null) leftForearm.xRot -= 0.8F;
        } else {
            float drop = legLength * 0.75F;
            for (ModelPart p : new ModelPart[] {body, head, rightArm, leftArm}) p.y += drop;
            rightLeg.y += drop;
            leftLeg.y += drop;
            rightLeg.xRot = -1.45F;
            leftLeg.xRot = -1.45F;
            rightLeg.yRot = 0.2F;
            leftLeg.yRot = -0.2F;
            head.xRot += 0.35F + Mth.sin(t * 0.05F) * 0.03F;
            rightArm.xRot -= 0.35F;
            leftArm.xRot -= 0.35F;
        }
    }
}
