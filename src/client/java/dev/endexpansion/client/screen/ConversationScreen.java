package dev.endexpansion.client.screen;

import dev.endexpansion.talk.TalkActionPayload;
import dev.endexpansion.talk.TalkPayload;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.input.KeyEvent;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * The conversation window: the Village Friends layout in purpur. The resident stays in view in the
 * world; a dialogue box with their portrait and name ribbon sits at the bottom, the line typing out
 * in their voice (glassy Shulkin chimes, a low Chorrin hum, the Court's warped bass); replies float
 * as numbered bubbles on the right; a dock offers talk, a gift (tribute, for the Court) and farewell;
 * and a card shows how close you are as ten chorus blossoms, or the Court's Favor as ten eyes.
 */
public final class ConversationScreen extends Screen {
    static final int PAPER = 0xFFF6EEF7, PAPER_SHADE = 0xFFE6D6E8, EDGE = 0xFF4A2C52, EDGE_LIGHT = 0xFFB48FB6, INK = 0xFF3B2544,
            MUTED = 0xFF8A7393, STATUS = 0xFF2F8F84, STATUS_NEW = 0xFF1F7A70, BLOSSOM = 0xFFC77DD6, BLOSSOM_LIGHT = 0xFFF0CDF5,
            EYE = 0xFFD659F5, EYE_HOT = 0xFFFBE3FF, EMPTY = 0xFFE0CFE3;
    /** Level badge colours by fifths of the way to 10. */
    static final int[] TIERS = {0xFF9A8AA0, 0xFF8E78B8, 0xFFA05FB8, 0xFFC055C0, 0xFFE07FD0};
    private static final float CHARS_PER_SECOND = 36F;
    private static final int SPACE_KEY = 32, KEY_1 = 49, LINE = 10;

    private TalkPayload data;
    private final List<Button> actions = new ArrayList<>();
    private boolean waiting, closing;
    private int waitTicks, ticks;
    private int boxX, boxY, boxW, boxH, textX, textW, portraitX, portraitY, portraitW, portraitH, cardX, cardY, cardW, cardH;
    private int dialogueScroll;
    private String lastDialogue;
    private List<String> typeLines = List.of();
    private int[] lineStarts = new int[0];
    private String typeKey = "", typeFlat = "";
    private int shown, sinceBlip;
    private float typeBudget, typePause;
    private long lastFrameNanos;
    private boolean popPending = true, wholeLines;
    private int levelUpAt = -1000, statusAt;

    public ConversationScreen(TalkPayload data) {
        super(Component.literal(data.name()));
        this.data = data;
        this.lastDialogue = data.dialogue();
    }

    public boolean matches(TalkPayload next) {
        return data.id().equals(next.id());
    }

    public TalkPayload data() {
        return data;
    }

    /** Whether the current line has been laid out and has finished typing out. */
    public boolean doneTyping() {
        return typeKey.startsWith(data.dialogue() + '|') && !typing();
    }

    /** Show every line whole instead of typing it out (tests, where frames are few and far between). */
    public void showWholeLines() {
        wholeLines = true;
        finishLine();
    }

    public void update(TalkPayload next) {
        if (!lastDialogue.equals(next.dialogue())) {
            dialogueScroll = 0;
            lastDialogue = next.dialogue();
            restartTyping();
        }
        if (next.levelUp()) {
            levelUpAt = ticks;
            playUi(SoundEvents.AMETHYST_BLOCK_CHIME, 1.6F, 0.8F);
        }
        if (!next.status().equals(data.status())) statusAt = ticks;
        data = next;
        waiting = false;
        waitTicks = 0;
        rebuildWidgets();
        triggerImmediateNarration(false);
    }

    private boolean court() {
        return data.voice().equals("court");
    }

    // -- typing ------------------------------------------------------------------------------------

    private void restartTyping() {
        shown = 0;
        typeBudget = 0;
        typePause = 0;
        sinceBlip = 0;
        popPending = true;
    }

    private boolean typing() {
        return shown < typeFlat.length();
    }

    private void finishLine() {
        if (typing()) shown = typeFlat.length();
    }

    private void playUi(SoundEvent sound, float pitch, float volume) {
        if (minecraft != null) minecraft.getSoundManager().play(SimpleSoundInstance.forUI(sound, pitch, volume));
    }

    /** One typing blip in the speaker's voice. */
    private void blip(char c) {
        float wobble = Character.toLowerCase(c) % 7 * 0.04F;
        switch (data.voice()) {
            case "chorrin" -> playUi(SoundEvents.NOTE_BLOCK_DIDGERIDOO.value(), 0.6F + wobble, 0.35F);
            case "chorrin_child" -> playUi(SoundEvents.NOTE_BLOCK_DIDGERIDOO.value(), 1.0F + wobble, 0.3F);
            case "court" -> playUi(SoundEvents.NOTE_BLOCK_BASS.value(), 0.5F + wobble * 0.5F, 0.4F);
            case "shulkin_child" -> playUi(SoundEvents.NOTE_BLOCK_CHIME.value(), 1.75F + wobble, 0.2F);
            default -> playUi(SoundEvents.NOTE_BLOCK_CHIME.value(), 1.35F + wobble, 0.22F);
        }
    }

    private void layoutTyping(int wrapWidth) {
        String key = data.dialogue() + '|' + wrapWidth;
        if (key.equals(typeKey)) return;
        typeKey = key;
        typeLines = font.splitIgnoringLanguage(Component.literal(data.dialogue()), wrapWidth).stream().map(t -> t.getString()).toList();
        lineStarts = new int[typeLines.size()];
        int total = 0;
        for (int i = 0; i < lineStarts.length; i++) {
            lineStarts[i] = total;
            total += typeLines.get(i).length();
        }
        typeFlat = String.join("", typeLines);
        shown = wholeLines ? total : Math.min(shown, total);
    }

    private void advanceTyping() {
        long now = System.nanoTime();
        float dt = lastFrameNanos == 0 ? 0F : Math.min(0.25F, (now - lastFrameNanos) / 1.0E9F);
        lastFrameNanos = now;
        if (popPending) {
            popPending = false;
            playUi(court() ? SoundEvents.ENDERMAN_AMBIENT : SoundEvents.AMETHYST_BLOCK_CHIME, court() ? 1.4F : 1.2F, 0.25F);
        }
        if (!typing()) return;
        typeBudget += dt;
        float cost = 1F / CHARS_PER_SECOND;
        while (typeBudget > 0 && typing()) {
            if (typePause > 0) {
                float used = Math.min(typePause, typeBudget);
                typePause -= used;
                typeBudget -= used;
                continue;
            }
            if (typeBudget < cost) break;
            typeBudget -= cost;
            char c = typeFlat.charAt(shown++);
            if (!Character.isWhitespace(c) && c != '*' && ++sinceBlip >= 2) {
                sinceBlip = 0;
                blip(c);
            }
            if (".!?".indexOf(c) >= 0) typePause = 0.18F;
            else if (",;:".indexOf(c) >= 0) typePause = 0.08F;
        }
    }

    // -- layout ------------------------------------------------------------------------------------

    @Override
    protected void init() {
        actions.clear();
        int dockH = 20, bottom = height - 8 - dockH - 5;
        boxW = Math.min(430, width - 16);
        boxX = (width - boxW) / 2;
        portraitW = 64;
        textX = boxX + portraitW + 18;
        textW = boxX + boxW - 12 - textX;
        int count = data.choices().size(), row = 18, baseH = 64;
        int columns = count * row > bottom - baseH - 30 ? 2 : 1;
        int rows = (count + columns - 1) / columns;
        int replyW = columns == 1 ? Math.clamp(width * 2 / 5, 130, 186) : Math.clamp((boxW - 12) / 2 - 2, 100, 170);
        boxH = baseH;
        boxY = bottom - boxH;
        portraitH = Math.min(boxH + 30, 118);
        portraitX = boxX + 7;
        portraitY = boxY + boxH - 7 - portraitH;
        cardX = 8;
        cardY = 8;
        cardW = Math.min(170, width / 2 - 12);
        cardH = 50;
        int replyRight = Math.max(boxX + boxW, width - 10), replyBottom = boxY - 18;
        for (int i = 0; i < count; i++) {
            var choice = data.choices().get(i);
            int column = columns == 1 ? 0 : i % 2, r = columns == 1 ? i : i / 2;
            int x = replyRight - (columns - column) * (replyW + 4) + 4, y = replyBottom - (rows - r) * row;
            var button = new ReplyButton(x, y, replyW, row - 3, i + 1, choice.label(), pressed -> send(choice.id()));
            button.active = !waiting && choice.enabled();
            if (!choice.hint().isEmpty()) button.setTooltip(Tooltip.create(Component.literal(choice.hint())));
            actions.add(button);
            addRenderableWidget(button);
        }
        // the dock: talk, a gift (or tribute), farewell
        var player = Minecraft.getInstance().player;
        ItemStack held = player == null ? ItemStack.EMPTY : player.getMainHandItem();
        String[] labels = {"Talk", data.giftLabel(), "Farewell"};
        String[] ids = {"talk", "gift", "goodbye"};
        ItemStack[] icons = {new ItemStack(court() ? Items.ENDER_EYE : Items.CHORUS_FLOWER),
                held.isEmpty() ? new ItemStack(court() ? Items.CRYING_OBSIDIAN : Items.POPPED_CHORUS_FRUIT) : held.copyWithCount(1),
                new ItemStack(Items.CRIMSON_DOOR)};
        boolean wide = width >= 360;
        int each = wide ? 78 : 22, gap = 4;
        int total = 3 * each + 2 * gap + 8, x = (width - total) / 2, y = height - 8 - dockH;
        for (int i = 0; i < 3; i++) {
            if (i == 2) x += 8;
            String id = ids[i];
            var button = new DockButton(x, y, each, dockH, labels[i], icons[i], wide, id.equals("gift") ? data.giftsLeft() : -1,
                    pressed -> {
                        if (id.equals("goodbye")) onClose();
                        else send(id);
                    });
            button.setTooltip(Tooltip.create(Component.literal(tooltip(id, held))));
            if (id.equals("gift")) button.active = !waiting && data.giftsLeft() > 0;
            else if (!id.equals("goodbye")) button.active = !waiting;
            if (!id.equals("goodbye")) actions.add(button);
            addRenderableWidget(button);
            x += each + gap;
        }
    }

    private String tooltip(String id, ItemStack held) {
        return switch (id) {
            case "talk" -> court() ? "Talk: begin the audience again" : "Talk: say hello again";
            case "gift" -> (court() ? "Tribute: offer " : "Gift: give ")
                    + (held.isEmpty() ? "what you hold in your main hand" : "one " + held.getHoverName().getString()) + ". " + data.giftsLeft() + " left today.";
            default -> "Farewell (Esc)";
        };
    }

    private void send(String action) {
        if (waiting || !ClientPlayNetworking.canSend(TalkActionPayload.TYPE)) return;
        ClientPlayNetworking.send(new TalkActionPayload(data.entityId(), data.id(), action));
        waiting = true;
        waitTicks = 0;
        actions.forEach(button -> button.active = false);
    }

    /** Presses a reply or dock button by id, as a click would (for tests). */
    public void press(String action) {
        send(action);
    }

    // -- input -------------------------------------------------------------------------------------

    @Override
    public boolean keyPressed(KeyEvent event) {
        if (event.key() == SPACE_KEY && typing()) {
            finishLine();
            return true;
        }
        int index = event.key() - KEY_1;
        if (index >= 0 && index < data.choices().size() && !waiting) {
            var choice = data.choices().get(index);
            if (choice.enabled()) {
                send(choice.id());
                return true;
            }
        }
        return super.keyPressed(event);
    }

    @Override
    public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (typing() && event.x() >= boxX && event.x() < boxX + boxW && event.y() >= boxY && event.y() < boxY + boxH) {
            finishLine();
            return true;
        }
        return super.mouseClicked(event, doubleClick);
    }

    @Override
    public boolean mouseScrolled(double x, double y, double horizontal, double vertical) {
        if (x >= boxX && x < boxX + boxW && y >= boxY && y < boxY + boxH) {
            dialogueScroll = Math.clamp(dialogueScroll - (int) Math.signum(vertical), 0, Math.max(0, typeLines.size() - visibleLines()));
            return true;
        }
        return super.mouseScrolled(x, y, horizontal, vertical);
    }

    @Override
    public void tick() {
        ticks++;
        if (minecraft.player == null || minecraft.level == null) {
            onClose();
            return;
        }
        var who = minecraft.level.getEntity(data.entityId());
        if (who == null || !who.isAlive() || !who.getUUID().equals(data.id()) || minecraft.player.distanceToSqr(who) > 64 || !minecraft.player.isAlive()) {
            onClose();
            return;
        }
        if (waiting && ++waitTicks > 100) {
            waiting = false;
            rebuildWidgets();
        }
    }

    /** Tell the resident the conversation is over, however the window closed. */
    @Override
    public void removed() {
        if (!closing && ClientPlayNetworking.canSend(TalkActionPayload.TYPE)) {
            closing = true;
            ClientPlayNetworking.send(new TalkActionPayload(data.entityId(), data.id(), "goodbye"));
        }
        super.removed();
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public boolean isInGameUi() {
        return true;
    }

    @Override
    public Component getNarrationMessage() {
        return Component.literal(data.name() + ", " + data.title() + ". " + (court() ? "Favor " : "Friendship ") + data.level() + ", "
                + data.levelName() + ". " + data.dialogue() + " " + data.status());
    }

    // -- drawing -----------------------------------------------------------------------------------

    /** No blur: the resident stays visible in the world; a soft violet shade lifts the text. */
    @Override
    public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fillGradient(0, height / 2, width, height, 0x00000000, 0x6612081A);
    }

    private int visibleLines() {
        return Math.max(1, (boxH - 24) / LINE);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        float now = ticks + delta;
        drawCard(g, mouseX, mouseY);
        panel(g, boxX, boxY, boxW, boxH, PAPER);
        frame(g, portraitX - 2, portraitY - 2, portraitW + 4, portraitH + 4);
        if (court()) g.fillGradient(portraitX, portraitY, portraitX + portraitW, portraitY + portraitH, 0xFF2C2242, 0xFF5A395B);
        else g.fillGradient(portraitX, portraitY, portraitX + portraitW, portraitY + portraitH, 0xFFE6D6E8, 0xFFFBF6E9);
        if (minecraft.level != null && minecraft.level.getEntity(data.entityId()) instanceof LivingEntity who) {
            // frame the head and shoulders whatever their height
            float h = who.getBbHeight(), eye = who.getEyeHeight();
            float span = Math.clamp(h * 0.55F, 1.0F, 1.9F);
            int size = (int) (portraitH / span);
            float yOffset = (eye - span * 0.32F) - h / 2.0F;
            InventoryScreen.extractEntityInInventoryFollowsMouse(g, portraitX, portraitY, portraitX + portraitW, portraitY + portraitH,
                    size, yOffset, portraitX + portraitW / 2F - 10, portraitY + portraitH / 3F, who);
        }
        drawRibbon(g, mouseX, mouseY);
        layoutTyping(textW);
        advanceTyping();
        int visible = visibleLines();
        if (typing()) {
            int lastLine = 0;
            for (int i = 0; i < lineStarts.length; i++) if (lineStarts[i] < shown) lastLine = i;
            dialogueScroll = Math.max(dialogueScroll, lastLine - visible + 1);
        }
        dialogueScroll = Math.clamp(dialogueScroll, 0, Math.max(0, typeLines.size() - visible));
        int top = boxY + 9;
        g.enableScissor(textX, top - 1, textX + textW, top + visible * LINE);
        for (int line = dialogueScroll, y = top; line < Math.min(typeLines.size(), dialogueScroll + visible); line++, y += LINE) {
            int chars = Math.min(typeLines.get(line).length(), shown - lineStarts[line]);
            if (chars <= 0) break;
            g.text(font, typeLines.get(line).substring(0, chars), textX, y, INK, false);
        }
        g.disableScissor();
        if (typeLines.size() > visible) scrollbar(g, top, visible);
        int statusY = boxY + boxH - 13;
        g.fill(textX, statusY - 3, textX + textW, statusY - 2, PAPER_SHADE);
        String status = waiting ? (court() ? "The Court considers..." : "Listening...") : data.status();
        g.text(font, font.plainSubstrByWidth(status, textW - 12), textX, statusY, now - statusAt < 40 ? STATUS_NEW : STATUS, false);
        if (mouseX >= textX && mouseX < textX + textW && mouseY >= statusY - 2 && mouseY < statusY + 9 && font.width(status) > textW - 12)
            g.setTooltipForNextFrame(Component.literal(status), mouseX, mouseY);
        if (!typing() && !waiting) {
            int bounce = (int) (Math.abs(Mth.sin(now * .25F)) * 2);
            int ax = boxX + boxW - 14, ay = statusY + 1 + bounce;
            for (int i = 0; i < 4; i++) g.fill(ax + i, ay + i, ax + 7 - i, ay + i + 1, EDGE_LIGHT);
        }
        super.extractRenderState(g, mouseX, mouseY, delta);
        drawLevelUp(g, now);
    }

    private void drawCard(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        panel(g, cardX, cardY, cardW, cardH, PAPER);
        int tier = TIERS[Math.clamp(data.level() / 2 - (data.level() == 10 ? 1 : 0), 0, 4)];
        String badge = (court() ? "Favor " : "Lv. ") + data.level();
        int badgeW = font.width(badge) + 10;
        pill(g, cardX + 6, cardY + 6, badgeW, 12, tier);
        g.text(font, badge, cardX + 11, cardY + 8, 0xFFFFFFFF, true);
        g.text(font, font.plainSubstrByWidth(data.levelName(), cardW - badgeW - 18), cardX + badgeW + 11, cardY + 8, INK, false);
        int floor = data.levelFloor(), next = Math.max(floor + 1, data.nextThreshold());
        float progress = data.level() >= 10 ? 0 : Math.clamp((data.points() - floor) / (float) (next - floor), 0, 1);
        int hx = cardX + 7, hy = cardY + 23;
        for (int i = 0; i < 10; i++) {
            float fill = i < data.level() ? 1 : i == data.level() ? progress : 0;
            if (court()) eye(g, hx + i * 9, hy, fill);
            else blossom(g, hx + i * 9, hy, fill);
        }
        String goal = data.level() >= 10 ? (court() ? "The Court can honour you no higher." : "As close as friends can be.")
                : (next - data.points()) + (court() ? " more Favor to the next eye" : " more to the next blossom");
        g.text(font, font.plainSubstrByWidth(goal, cardW - 12), cardX + 6, cardY + 35, MUTED, false);
        if (mouseX >= cardX && mouseX < cardX + cardW && mouseY >= cardY && mouseY < cardY + cardH) {
            var lines = new ArrayList<Component>();
            lines.add(Component.literal((court() ? "Favor " : "Friendship ") + data.level() + " of 10: " + data.levelName()));
            lines.add(Component.literal(data.points() + (court() ? " Favor with " : " friendship with ") + data.name()));
            if (court()) lines.add(Component.literal("Favor is kept by the whole Court of " + data.home() + "."));
            g.setComponentTooltipForNextFrame(font, lines, mouseX, mouseY);
        }
    }

    private int ribbonColour() {
        return switch (data.voice()) {
            case "chorrin" -> 0xFF8E8A55;
            case "chorrin_child" -> 0xFFA9A86E;
            case "court" -> 0xFF2C2242;
            case "shulkin_child" -> 0xFFB68FB8;
            default -> 0xFF8F5F91;
        };
    }

    private void drawRibbon(GuiGraphicsExtractor g, int mouseX, int mouseY) {
        int color = ribbonColour();
        String name = font.plainSubstrByWidth(data.name(), boxW - portraitW - 40);
        int w = font.width(name) + 14, x = textX - 4, y = boxY - 12;
        g.fill(x + 1, y + 1, x + w + 1, y + 14, 0x55000000);
        g.fill(x, y, x + w, y + 13, color);
        g.fill(x, y + 11, x + w, y + 13, darker(color));
        g.fill(x - 1, y + 1, x, y + 12, darker(color));
        g.fill(x + w, y + 1, x + w + 1, y + 12, darker(color));
        g.text(font, name, x + 7, y + 3, 0xFFFFFFFF, true);
        String subtitle = data.title() + " · " + data.home();
        int room = boxX + boxW - (x + w + 6) - 6;
        if (room > 40) g.text(font, font.plainSubstrByWidth(subtitle, room), x + w + 6, y + 3, 0xFFF6EEF7, true);
        if (mouseX >= x && mouseX < x + w && mouseY >= y && mouseY < y + 13) g.setTooltipForNextFrame(Component.literal(subtitle), mouseX, mouseY);
    }

    /** A banner that drops in when you grow closer. */
    private void drawLevelUp(GuiGraphicsExtractor g, float now) {
        float age = now - levelUpAt;
        if (age < 0 || age > 80) return;
        float drop = age < 8 ? 1 - (float) Math.pow(1 - age / 8, 3) : age > 70 ? 1 - (age - 70) / 10 : 1;
        String title = data.levelName() + "!";
        String sub = (court() ? "Favor " : "Friendship ") + data.level() + " of 10";
        int w = Math.max(font.width(title), font.width(sub)) + 40, h = 30, x = (width - w) / 2, y = (int) (-h + (h + 10) * drop);
        panel(g, x, y, w, h, 0xFFFBF2FC);
        g.centeredText(font, title, width / 2, y + 6, court() ? 0xFF8F2FB0 : BLOSSOM);
        g.centeredText(font, sub, width / 2, y + 17, INK);
        for (int i = 0; i < 6; i++) {
            float a = age * .12F + i * 1.047F;
            int sx = (int) (width / 2 + Mth.cos(a) * (w / 2F + 6)), sy = (int) (y + h / 2 + Mth.sin(a) * (h / 2F + 5));
            if (court()) eye(g, sx - 3, sy - 3, 1);
            else blossom(g, sx - 3, sy - 3, 1);
        }
    }

    private void scrollbar(GuiGraphicsExtractor g, int top, int visible) {
        int trackX = boxX + boxW - 6, trackH = visible * LINE;
        g.fill(trackX, top, trackX + 2, top + trackH, PAPER_SHADE);
        int thumb = Math.max(6, trackH * visible / typeLines.size());
        int offset = (trackH - thumb) * dialogueScroll / Math.max(1, typeLines.size() - visible);
        g.fill(trackX, top + offset, trackX + 2, top + offset + thumb, EDGE_LIGHT);
    }

    // -- drawing helpers ---------------------------------------------------------------------------

    /** A rounded paper panel with a dark purpur edge and a soft drop shadow. */
    static void panel(GuiGraphicsExtractor g, int x, int y, int w, int h, int paper) {
        g.fill(x + 1, y + h, x + w - 1, y + h + 2, 0x55000000);
        g.fill(x + 1, y, x + w - 1, y + h, EDGE);
        g.fill(x, y + 1, x + w, y + h - 1, EDGE);
        g.fill(x + 2, y + 1, x + w - 2, y + h - 1, paper);
        g.fill(x + 1, y + 2, x + w - 1, y + h - 2, paper);
        g.fill(x + 2, y + h - 3, x + w - 2, y + h - 2, PAPER_SHADE);
        g.fill(x + 2, y + 2, x + w - 2, y + 3, 0xFFFFFFFF);
    }

    static void frame(GuiGraphicsExtractor g, int x, int y, int w, int h) {
        g.fill(x + 1, y + h, x + w + 1, y + h + 2, 0x55000000);
        g.fill(x, y, x + w, y + h, EDGE);
        g.fill(x + 1, y + 1, x + w - 1, y + h - 1, EDGE_LIGHT);
    }

    static void pill(GuiGraphicsExtractor g, int x, int y, int w, int h, int color) {
        g.fill(x + 1, y, x + w - 1, y + h, color);
        g.fill(x, y + 1, x + w, y + h - 1, color);
        g.fill(x + 1, y + h - 2, x + w - 1, y + h - 1, darker(color));
    }

    static int darker(int color) {
        int r = (color >> 16 & 255) * 3 / 4, gr = (color >> 8 & 255) * 3 / 4, b = (color & 255) * 3 / 4;
        return 0xFF000000 | r << 16 | gr << 8 | b;
    }

    /** A 7x7 chorus blossom, filled from the left by {@code fill} (0 to 1). */
    static void blossom(GuiGraphicsExtractor g, int x, int y, float fill) {
        int[] masks = {0b0011100, 0b0110110, 0b1101011, 0b1110111, 0b1101011, 0b0110110, 0b0011100};
        for (int row = 0; row < masks.length; row++) for (int col = 0; col < 7; col++) {
            if ((masks[row] & (1 << (6 - col))) == 0) continue;
            boolean filled = col < Math.round(Math.clamp(fill, 0, 1) * 7);
            boolean heart = row == 3 && col == 3;
            int c = filled ? heart ? 0xFFFFF4C8 : row <= 2 && col < 4 ? BLOSSOM_LIGHT : BLOSSOM : EMPTY;
            g.fill(x + col, y + row, x + col + 1, y + row + 1, c);
        }
    }

    /** A 7x5 Court eye, opened from the left by {@code fill}. */
    static void eye(GuiGraphicsExtractor g, int x, int y, float fill) {
        int[] masks = {0b0011100, 0b0111110, 0b1111111, 0b0111110, 0b0011100};
        for (int row = 0; row < masks.length; row++) for (int col = 0; col < 7; col++) {
            if ((masks[row] & (1 << (6 - col))) == 0) continue;
            boolean filled = col < Math.round(Math.clamp(fill, 0, 1) * 7);
            boolean pupil = row == 2 && (col == 3);
            int c = filled ? pupil ? 0xFF1B1430 : row == 1 && col < 4 ? EYE_HOT : EYE : 0xFF2C2242;
            g.fill(x + col, y + row + 1, x + col + 1, y + row + 2, c);
        }
    }

    /** A numbered reply bubble. */
    static final class ReplyButton extends Button {
        private final int number;

        ReplyButton(int x, int y, int w, int h, int number, String label, OnPress action) {
            super(x, y, w, h, Component.literal(label), action, DEFAULT_NARRATION);
            this.number = number;
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
            boolean hover = active && isHoveredOrFocused();
            int x = getX() + (hover ? -2 : 0), y = getY(), w = getWidth(), h = getHeight();
            int paper = !active ? 0xFFE3D6E5 : hover ? 0xFFFFFFFF : 0xFFF9F2FA;
            int edge = active ? EDGE : 0xFFA592A8;
            g.fill(x + 2, y + h, x + w - 2, y + h + 1, 0x44000000);
            g.fill(x + 2, y, x + w - 2, y + h, edge);
            g.fill(x + 1, y + 1, x + w - 1, y + h - 1, edge);
            g.fill(x + 2, y + 1, x + w - 2, y + h - 1, paper);
            g.fill(x + 1, y + 2, x + w - 1, y + h - 2, paper);
            int badge = active ? hover ? BLOSSOM : EDGE_LIGHT : 0xFFB9A9BC;
            g.fill(x + 3, y + 2, x + 12, y + h - 2, badge);
            var font = Minecraft.getInstance().font;
            g.centeredText(font, String.valueOf(number), x + 8, y + (h - 8) / 2, 0xFFFFFFFF);
            String label = font.plainSubstrByWidth(getMessage().getString(), w - 20);
            g.text(font, label, x + 16, y + (h - 8) / 2, active ? INK : 0xFF9A8A9E, false);
        }
    }

    /** A round dock button with an item icon (and its name, on wide screens). */
    static final class DockButton extends Button {
        private final ItemStack icon;
        private final boolean labeled;
        private final int badge;

        DockButton(int x, int y, int w, int h, String label, ItemStack icon, boolean labeled, int badge, OnPress action) {
            super(x, y, w, h, Component.literal(label), action, DEFAULT_NARRATION);
            this.icon = icon;
            this.labeled = labeled;
            this.badge = badge;
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
            boolean hover = active && isHoveredOrFocused();
            int x = getX(), y = getY() - (hover ? 1 : 0), w = getWidth(), h = getHeight();
            int fill = !active ? 0xFFD9CCDB : hover ? 0xFFFFFFFF : 0xFFF1E6F3;
            int edge = !active ? 0xFFA592A8 : EDGE;
            g.fill(x + 2, y + h, x + w - 2, y + h + 2, 0x44000000);
            g.fill(x + 2, y, x + w - 2, y + h, edge);
            g.fill(x, y + 2, x + w, y + h - 2, edge);
            g.fill(x + 1, y + 1, x + w - 1, y + h - 1, edge);
            g.fill(x + 2, y + 1, x + w - 2, y + h - 1, fill);
            g.fill(x + 1, y + 2, x + w - 1, y + h - 2, fill);
            int iconX = labeled ? x + 3 : x + (w - 16) / 2, iconY = y + (h - 16) / 2;
            if (!icon.isEmpty()) g.item(icon, iconX, iconY);
            var font = Minecraft.getInstance().font;
            if (labeled) g.text(font, font.plainSubstrByWidth(getMessage().getString(), w - 22), x + 20, y + (h - 8) / 2, active ? INK : 0xFF9A8A9E, false);
            if (badge >= 0) {
                int bx = x + w - 7, by = y - 3;
                g.fill(bx - 1, by, bx + 7, by + 8, badge > 0 ? BLOSSOM : 0xFF9A8AA0);
                g.centeredText(font, String.valueOf(badge), bx + 3, by, 0xFFFFFFFF);
            }
            if (!active) g.fill(x + 2, y + 2, x + w - 2, y + h - 2, 0x66E3D6E5);
        }
    }
}
