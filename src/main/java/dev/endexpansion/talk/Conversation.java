package dev.endexpansion.talk;

import dev.endexpansion.EndEntities;
import dev.endexpansion.anim.Cue;
import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.entity.EndFolk;
import dev.endexpansion.entity.Endarch;
import dev.endexpansion.entity.EndermanThrall;
import dev.endexpansion.entity.Voidhound;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.ShulkerBoxBlock;
import org.jspecify.annotations.Nullable;

/**
 * The server side of a conversation: what the resident says when you open it, and what happens for
 * each reply (topics), gift or tribute, Court service, and the Lord's hound. Each step sends the
 * whole screen state ({@link TalkPayload}); the client sends back the button pressed
 * ({@link TalkActionPayload}).
 *
 * <p>Closeness grows a little the first time you talk each day and for each topic once a day, and
 * with gifts the resident likes (two a day). The Court counts Favor per Citadel and also sets
 * service tasks: bring what they ask for and Favor grows. At eight eyes of Favor the Lord gives
 * you a Voidhound pup, once per Citadel.
 *
 * <p>The screen has three tabs: Talk (the replies above), Story (their personal story, see
 * {@link Storyteller}) and Journal (your memories with them and what you know of them). Someone
 * who is still upset with you, or busy, or woken at night, or (the Court) unimpressed, may cut the
 * conversation short ({@link #walkOff}); see {@code EndFolk} for who and when.
 */
public final class Conversation {
    public static final int GIFTS_PER_DAY = 2;
    public static final int HOUND_LEVEL = 8;
    private static final double REACH = 8.0;

    /** Court service tasks: what to bring, how many, how much Favor, and how the Court names it. */
    public record Task(String id, Item item, int count, int favor, String words) {}

    public static final List<Task> TASKS = List.of(
            task("obsidian", 16, 8, "sixteen blocks of obsidian"),
            task("crying_obsidian", 8, 10, "eight blocks of crying obsidian"),
            task("ender_pearl", 8, 10, "eight ender pearls"),
            task("purpur_block", 32, 7, "thirty-two blocks of purpur"),
            task("end_stone_bricks", 32, 6, "thirty-two end stone bricks"),
            task("end_rod", 8, 8, "eight end rods"),
            task("shulker_shell", 2, 12, "two shulker shells"),
            task("end_crystal", 1, 14, "an end crystal"),
            task("amethyst_shard", 16, 7, "sixteen amethyst shards"),
            task("iron_ingot", 24, 8, "twenty-four iron ingots"),
            task("blaze_rod", 6, 10, "six blaze rods"),
            task("chorus_fruit", 32, 5, "thirty-two chorus fruit for the thralls"));

    private static Task task(String item, int count, int favor, String words) {
        return new Task(item, BuiltInRegistries.ITEM.getValue(Identifier.withDefaultNamespace(item)), count, favor, words);
    }

    private Conversation() {}

    public static void register() {
        PayloadTypeRegistry.clientboundPlay().register(TalkPayload.TYPE, TalkPayload.CODEC);
        PayloadTypeRegistry.serverboundPlay().register(TalkActionPayload.TYPE, TalkActionPayload.CODEC);
        ServerPlayNetworking.registerGlobalReceiver(TalkActionPayload.TYPE, (payload, context) -> act(context.player(), payload));
    }

    // -- opening ----------------------------------------------------------------------------------

    public static void open(ServerPlayer player, EndFolk folk) {
        if (folk.getTarget() != null) return;
        boolean court = folk instanceof Endarch;
        if (court && !CitadelLaw.isGuest(player, folk)) {
            if (!CitadelLaw.isOutlaw(player, folk)) narrate(player, folk.getName().getString() + " will not speak with one who does not bear the Eyes.");
            return;
        }
        String snub = folk.snubbedBy(player);
        if (snub != null) {
            String first = folk.firstName();
            player.sendOverlayMessage(Component.literal(switch (snub) {
                case "dislike" -> first + " turns away from you.";
                case "sleep" -> first + " is asleep.";
                case "dismissed" -> folk.getName().getString() + " will not grant you another audience just yet.";
                default -> first + " is busy. Try again in a little while.";
            }));
            return;
        }
        ServerLevel level = player.level();
        Bond bond = folk.bond(player);
        long day = folk.dayNumber();
        bond.today(day);
        Tale tale = folk.tale(player);
        tale.visit(day);
        int before = folk.meter().level(bond.points);
        String topic;
        if (!bond.met || tale.memories.isEmpty()) {
            tale.remember(day, court ? "Received by " + folk.getName().getString() + " in " + folk.settlement().name() + "."
                    : "Met " + folk.firstName() + " in " + folk.settlement().name() + ".");
        }
        boolean upset = !court && bond.grudge > 0;
        if (!bond.met) {
            topic = "first_meeting";
            bond.met = true;
        } else if (bond.hurtUntil > level.getGameTime()) {
            topic = court ? "greeting" : "hurt";
        } else if (folk.isSleeping()) {
            topic = "night";
        } else if (!court && carriesShulkerBox(player) && folk.getRandom().nextInt(5) < 3) {
            topic = "shulker_box";
        } else if (!court && CitadelLaw.carriesEyes(player) && folk.getRandom().nextInt(2) == 0) {
            topic = "eyes";
        } else {
            topic = "greeting";
        }
        String status = "";
        if (upset) {
            status = folk.firstName() + " is still upset with you.";
        } else if (!bond.greeted) {
            bond.greeted = true;
            int gain = court ? 2 : 4;
            gain(folk, bond, gain);
            status = (court ? "An audience today: Favor +" : "First words today: +") + gain;
        }
        folk.startTalking(player);
        // someone upset with you is cool about it, whatever they once thought of you
        String said = upset && topic.equals("greeting") ? sayAt(folk, player, topic, bond, 0) : say(folk, player, topic, bond);
        send(player, folk, bond, talkPage(folk, bond, said, status), before, true, false);
    }

    /**
     * They cut the conversation short: they say so, and the screen shows it (the replies close).
     * {@code reason}: dislike (still upset with you), busy, sleep (woken at night) or dismissed (the Court).
     */
    public static void walkOff(ServerPlayer player, EndFolk folk, String reason) {
        Bond bond = folk.bond(player);
        long day = folk.dayNumber();
        bond.today(day);
        Tale tale = folk.tale(player);
        String topic = switch (reason) {
            case "dislike" -> "walk_off";
            case "sleep" -> "night";
            case "dismissed" -> "dismissed";
            default -> "busy_off";
        };
        String first = folk.firstName();
        String status = switch (reason) {
            case "dislike" -> first + " turned away. They're still upset with you.";
            case "sleep" -> first + " has gone back to sleep.";
            case "dismissed" -> "The audience is over.";
            default -> folk.isChild() ? first + " ran off to play." : first + " had to go.";
        };
        if (reason.equals("dislike")) tale.remember(day, first + " turned away from you.");
        if (reason.equals("dismissed")) tale.remember(day, folk.getName().getString() + " ended your audience.");
        int level = folk.meter().level(bond.points);
        String said = reason.equals("dislike") ? sayAt(folk, player, topic, bond, 0) : say(folk, player, topic, bond);
        Cue.send(folk, reason.equals("dislike") ? "annoyed" : "farewell", player);
        send(player, folk, bond, talkPage(folk, bond, said, status), level, false, true);
    }

    /** An Enderman thrall won't talk: a line of narration instead. */
    public static void thrall(ServerPlayer player, EndermanThrall thrall) {
        String line = DialogueBank.get("court").pick("thrall", 0, null, null, thrall.getRandom(), thrall.lastLine);
        if (line == null) return;
        thrall.lastLine = line;
        narrate(player, line);
    }

    private static void narrate(ServerPlayer player, String text) {
        player.sendSystemMessage(Component.literal(text).withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
    }

    // -- replies ----------------------------------------------------------------------------------

    static void act(ServerPlayer player, TalkActionPayload action) {
        if (!(player.level().getEntity(action.entityId()) instanceof EndFolk folk) || !folk.getUUID().equals(action.id()) || !folk.isAlive()) return;
        String act = action.action();
        boolean talking = folk.isTalkingTo(player);
        if (act.equals("goodbye")) {
            if (talking) folk.stopTalking();
            return;
        }
        // the Journal is the player's own: it stays open after they've cut the conversation short
        boolean journal = act.equals("tab_journal") || act.startsWith("journal_");
        double reach = journal ? REACH * 4 : REACH;
        if (folk.distanceToSqr(player) > reach * reach || (!talking && !journal)) return;
        boolean court = folk instanceof Endarch;
        if (court && talking && !CitadelLaw.isGuest(player, folk)) {
            folk.stopTalking();
            return;
        }
        if (talking) folk.keepTalking();
        Bond bond = folk.bond(player);
        long day = folk.dayNumber();
        bond.today(day);
        Tale tale = folk.tale(player);
        int before = folk.meter().level(bond.points);
        if (journal) {
            String page = act.startsWith("journal_") ? act.substring(8) : "memories";
            send(player, folk, bond, Storyteller.journal(folk, player, bond, tale, page), before, false, !talking);
            return;
        }
        if (act.equals("tab_story") || act.startsWith("story_")) {
            Storyteller.Page page = act.equals("tab_story") ? Storyteller.story(folk, player, bond, tale) : Storyteller.act(folk, player, bond, tale, act);
            if (page == null) return;
            folk.lastLine = page.text();
            folk.planLeave(player);
            send(player, folk, bond, page, before, false, false);
            return;
        }
        String said, status = "";
        switch (act) {
            case "talk", "tab_talk" -> said = say(folk, player, "greeting", bond);
            case "apology" -> {
                if (court || bond.grudge <= 0 || bond.apologized) return;
                bond.apologized = true;
                bond.grudge--;
                String first = folk.firstName();
                Cue.send(folk, bond.grudge == 0 ? "pleased" : "decline", player);
                if (bond.grudge == 0) {
                    said = say(folk, player, "apology_accepted", bond);
                    status = first + " forgives you.";
                    tale.remember(day, "You said sorry to " + first + ". They forgave you.");
                } else {
                    said = sayAt(folk, player, "apology_wary", bond, 0);
                    status = first + " is still wary of you. Give it time.";
                    tale.remember(day, "You said sorry to " + first + ". They're still wary.");
                }
            }
            case "gift" -> {
                String[] out = gift(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            case "service" -> {
                String[] out = service(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            case "hound" -> {
                String[] out = hound(player, folk, bond);
                said = out[0];
                status = out[1];
            }
            default -> {
                if (!topics(folk).contains(act)) return;
                String topic = act.equals("peoples") ? (folk.getRandom().nextBoolean() ? "shulkin" : "chorrin") : act;
                said = say(folk, player, topic, bond);
                if (bond.topics.add(act)) {
                    int gain = court ? 1 : action.action().equals("chat") ? 4 : 3;
                    gain(folk, bond, gain);
                    status = (court ? "Favor +" : "+") + gain;
                } else {
                    status = "You have talked about that today.";
                }
            }
        }
        folk.planLeave(player);
        send(player, folk, bond, talkPage(folk, bond, said, status), before, false, false);
    }

    private static String[] gift(ServerPlayer player, EndFolk folk, Bond bond) {
        boolean court = folk instanceof Endarch;
        String prefix = court ? "tribute_" : "gift_";
        ItemStack held = player.getMainHandItem();
        if (held.isEmpty()) return new String[] {folk.lastLine, "Hold something in your hand to " + (court ? "offer it." : "give it.")};
        if (bond.gifts >= GIFTS_PER_DAY) return new String[] {say(folk, player, prefix + "limit", bond), "No more " + (court ? "tribute" : "gifts") + " today."};
        String taste = DialogueBank.get(folk.bank()).taste(held);
        int points = switch (taste) {
            case "loved" -> court ? 8 : 25;
            case "liked" -> court ? 4 : 12;
            case "disliked" -> court ? -3 : -8;
            default -> court ? 1 : 4;
        };
        String name = held.getHoverName().getString();
        String id = BuiltInRegistries.ITEM.getKey(held.getItem()).toString();
        if (!player.hasInfiniteMaterials()) held.shrink(1);
        bond.gifts++;
        gain(folk, bond, points);
        Cue.send(folk, switch (taste) {
            case "loved" -> "happy";
            case "disliked" -> "decline";
            default -> "thanks";
        }, player);
        Tale tale = folk.tale(player);
        long day = folk.dayNumber();
        String first = folk.firstName();
        if (!taste.equals("neutral")) tale.tastes.put(id, taste);
        String gave = (court ? "Offered " : "Gave ") + first + " " + name + ". ";
        switch (taste) {
            case "loved" -> tale.remember(day, gave + (court ? "It was esteemed." : "They loved it."));
            case "liked" -> tale.remember(day, gave + (court ? "It was accepted." : "They liked it."));
            case "disliked" -> tale.remember(day, gave + (court ? "It was scorned." : "They didn't like it."));
            default -> { }
        }
        if (taste.equals("loved") && bond.grudge > 0) bond.grudge--;
        player.level().playSound(null, folk.blockPosition(), SoundEvents.ITEM_PICKUP, SoundSource.NEUTRAL, 0.6F, 1.1F);
        String verdict = switch (taste) {
            case "loved" -> "They loved the " + name + "!";
            case "liked" -> "They liked the " + name + ".";
            case "disliked" -> "They didn't like the " + name + ".";
            default -> "They took the " + name + ".";
        };
        return new String[] {say(folk, player, prefix + taste, bond), verdict + " " + (points >= 0 ? "+" : "") + points};
    }

    private static String[] service(ServerPlayer player, EndFolk folk, Bond bond) {
        Task task = task(bond.task);
        if (task == null) {
            task = TASKS.get(folk.getRandom().nextInt(TASKS.size()));
            bond.task = task.id();
            return new String[] {say(folk, player, "service_offer", bond), "The Court asks for " + task.words() + "."};
        }
        if (count(player, task.item()) >= task.count() || player.hasInfiniteMaterials()) {
            if (!player.hasInfiniteMaterials()) take(player, task.item(), task.count());
            gain(folk, bond, task.favor());
            String said = say(folk, player, "service_done", bond);
            bond.task = "";
            folk.tale(player).remember(folk.dayNumber(), "Served the Court of " + folk.settlement().name() + ": brought " + task.words() + ".");
            return new String[] {said, "Service done: Favor +" + task.favor()};
        }
        return new String[] {say(folk, player, "service_waiting", bond),
                "Bring " + task.words() + " (you have " + count(player, task.item()) + ")."};
    }

    private static String[] hound(ServerPlayer player, EndFolk folk, Bond bond) {
        int level = folk.meter().level(bond.points);
        if (bond.hound) return new String[] {say(folk, player, "hound_already", bond), "This Court has given you its hound."};
        if (level < HOUND_LEVEL) return new String[] {say(folk, player, "hound_low", bond), "The Lord gives a hound at " + HOUND_LEVEL + " eyes of Favor."};
        Voidhound pup = EndEntities.VOIDHOUND.create(player.level(), EntitySpawnReason.MOB_SUMMONED);
        if (pup == null) return new String[] {folk.lastLine, ""};
        pup.snapTo(player.getX(), player.getY(), player.getZ(), player.getYRot(), 0.0F);
        pup.makePup(player);
        player.level().addFreshEntity(pup);
        bond.hound = true;
        folk.tale(player).remember(folk.dayNumber(), folk.getName().getString() + " gave you a Voidhound pup.");
        return new String[] {say(folk, player, "hound_given", bond), "A Voidhound pup is yours."};
    }

    // -- helpers ----------------------------------------------------------------------------------

    /** The replies offered by each kind of person. */
    public static List<String> topics(EndFolk folk) {
        if (folk instanceof Endarch e) {
            List<String> out = new ArrayList<>(List.of("chat", "law", "dragon", "thralls", "peoples", "secret", "service"));
            if (e.job().equals("lord")) out.add("hound");
            return out;
        }
        String own = folk.people().equals("shulkin") ? "ancestors" : "void";
        return folk.isChild()
                ? List.of("chat", "play", "dragon", "village", "other", "court", own, "overworld")
                : List.of("chat", "dragon", "work", "village", "other", "court", own, "overworld");
    }

    private static String label(EndFolk folk, String topic, Bond bond) {
        return switch (topic) {
            case "chat" -> folk instanceof Endarch ? "Address them" : "Chat";
            case "play" -> "Play together";
            case "dragon" -> folk instanceof Endarch ? "Speak of the Dragon" : "Ask about the Dragon";
            case "work" -> "Ask about their work";
            case "village" -> "Ask about home";
            case "other" -> folk.people().equals("shulkin") ? "Ask about the Chorrin" : "Ask about the Shulkin";
            case "court" -> "Ask about the Court";
            case "ancestors" -> "Ask about the old shells";
            case "void" -> "Ask about the void";
            case "overworld" -> "Tell of the Overworld";
            case "law" -> "Ask about the law";
            case "thralls" -> "Ask about the thralls";
            case "peoples" -> "Ask of the other peoples";
            case "secret" -> "Ask where Endarchs come from";
            case "service" -> {
                Task t = task(bond.task);
                yield t == null ? "Offer your service" : "Deliver " + t.words();
            }
            case "hound" -> "Ask for a hound";
            case "apology" -> "Say you're sorry";
            default -> topic;
        };
    }

    private static @Nullable Task task(String id) {
        for (Task t : TASKS) if (t.id().equals(id)) return t;
        return null;
    }

    static int count(ServerPlayer player, Item item) {
        int n = 0;
        for (ItemStack s : player.getInventory()) if (s.is(item)) n += s.getCount();
        return n;
    }

    static void take(ServerPlayer player, Item item, int count) {
        for (ItemStack s : player.getInventory()) {
            if (count <= 0) return;
            if (!s.is(item)) continue;
            int used = Math.min(count, s.getCount());
            s.shrink(used);
            count -= used;
        }
    }

    public static boolean carriesShulkerBox(ServerPlayer player) {
        return player.getInventory().contains(s -> s.getItem() instanceof BlockItem b && b.getBlock() instanceof ShulkerBoxBlock);
    }

    static void gain(EndFolk folk, Bond bond, int points) {
        bond.points = Math.clamp(bond.points + points, 0, folk.meter().cap());
    }

    /** A line on a topic at the bond's level, placeholders filled. */
    static String say(EndFolk folk, ServerPlayer player, String topic, Bond bond) {
        return sayAt(folk, player, topic, bond, folk.meter().level(bond.points));
    }

    /** A line on a topic as if at {@code level}. */
    static String sayAt(EndFolk folk, ServerPlayer player, String topic, Bond bond, int level) {
        DialogueBank bank = DialogueBank.get(folk.bank());
        boolean court = folk.people().equals("court");
        String line = bank.pick(topic, level, court ? folk.job() : null, court ? null : folk.job(), folk.getRandom(), folk.lastLine);
        if (line == null) line = bank.pick("greeting", level, court ? folk.job() : null, null, folk.getRandom(), folk.lastLine);
        if (line == null) line = "...";
        String filled = DialogueBank.fill(line, vars(folk, player, bond));
        folk.lastLine = filled;
        return filled;
    }

    static Map<String, String> vars(EndFolk folk, ServerPlayer player, Bond bond) {
        Map<String, String> v = new HashMap<>();
        v.put("player", player.getName().getString());
        v.put("name", folk.firstName());
        v.put("village", folk.settlement().name());
        v.put("job", folk.title().toLowerCase(java.util.Locale.ROOT));
        v.put("title", folk.title());
        v.put("neighbour", neighbour(folk));
        Task t = task(bond.task);
        v.put("task", t == null ? "what the Court asks" : t.words());
        v.put("lord", lord(folk));
        return v;
    }

    /** Another resident of the same village by first name (made up if nobody is near). */
    private static String neighbour(EndFolk folk) {
        var near = folk.level().getEntitiesOfClass(EndFolk.class, folk.getBoundingBox().inflate(64),
                o -> o != folk && !o.firstName().isEmpty() && o.people().equals(folk.people()) && o.settlement().key().equals(folk.settlement().key()));
        if (!near.isEmpty()) return near.get(folk.getRandom().nextInt(near.size())).firstName();
        var names = DialogueBank.get(folk.people()).names();
        return names.isEmpty() ? "someone" : names.get(folk.getRandom().nextInt(names.size()));
    }

    private static String lord(EndFolk folk) {
        if (folk instanceof Endarch e && e.job().equals("lord")) return e.firstName();
        var lords = folk.level().getEntitiesOfClass(Endarch.class, folk.getBoundingBox().inflate(128),
                o -> o.job().equals("lord") && o.settlement().key().equals(folk.settlement().key()));
        if (!lords.isEmpty()) return lords.getFirst().firstName();
        RandomSource r = RandomSource.create(folk.settlement().key().hashCode());
        var names = DialogueBank.get("court").names();
        return names.isEmpty() ? "of the Citadel" : names.get(r.nextInt(names.size()));
    }

    /** The Talk tab: what they said, and the replies (a sorry first while they're upset with you). */
    private static Storyteller.Page talkPage(EndFolk folk, Bond bond, String said, String status) {
        int level = folk.meter().level(bond.points);
        List<String> topics = new ArrayList<>(topics(folk));
        if (!(folk instanceof Endarch) && bond.grudge > 0 && !bond.apologized) {
            topics.addFirst("apology");
            while (topics.size() > TalkPayload.MAX_CHOICES) topics.removeLast();
        }
        List<TalkPayload.Choice> choices = new ArrayList<>();
        for (String topic : topics) {
            String hint = "";
            if (topic.equals("hound") && !bond.hound && level < HOUND_LEVEL) hint = "The Lord gives a hound at " + HOUND_LEVEL + " eyes of Favor.";
            if (topic.equals("apology")) hint = "They're upset with you for striking them.";
            choices.add(new TalkPayload.Choice(topic, label(folk, topic, bond), true, hint));
        }
        return new Storyteller.Page("talk", said, status, choices);
    }

    /**
     * Sends the screen: {@code left} when they have cut it short (the replies close; only the Journal
     * still answers).
     */
    private static void send(ServerPlayer player, EndFolk folk, Bond bond, Storyteller.Page page, int levelBefore, boolean opening, boolean left) {
        Meter meter = folk.meter();
        int level = meter.level(bond.points);
        boolean levelUp = level > levelBefore;
        DialogueBank bank = DialogueBank.get(folk.bank());
        Tale tale = folk.tale(player);
        String dialogue = page.text();
        if (levelUp) {
            Cue.send(folk, "happy", player);
            String up = bank.pick("level_up", level, folk.people().equals("court") ? folk.job() : null, null, folk.getRandom(), null);
            // in their story and your Journal the banner says it; the quip is for small talk
            if (up != null && page.tab().equals("talk")) dialogue = dialogue + " " + DialogueBank.fill(up, vars(folk, player, bond));
            tale.remember(folk.dayNumber(), folk instanceof Endarch
                    ? "The Court of " + folk.settlement().name() + " now counts you " + bank.levelName(level) + "."
                    : "You and " + folk.firstName() + " grew closer: " + bank.levelName(level) + ".");
        }
        List<TalkPayload.Choice> choices = page.choices();
        if (left) {
            choices = choices.stream().map(c -> c.id().startsWith("journal_")
                    ? c : new TalkPayload.Choice(c.id(), c.label(), false, "They've gone.")).toList();
        }
        ServerPlayNetworking.send(player, new TalkPayload(folk.getId(), folk.getUUID(), folk.getName().getString(), folk.title(),
                folk.settlement().name(), folk.bank(), meter.id, level, bank.levelName(level), bond.points, meter.floor(level),
                meter.next(level), dialogue, page.status(), choices, Math.max(0, GIFTS_PER_DAY - bond.gifts),
                folk instanceof Endarch ? "Tribute" : "Gift", levelUp, opening, page.tab(), left,
                !left && Storyteller.alert(folk, player, bond, tale)));
    }
}
