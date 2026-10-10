package dev.endexpansion.talk;

import dev.endexpansion.entity.EndFolk;
import dev.endexpansion.entity.Endarch;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.Prediction;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import org.jspecify.annotations.Nullable;

/**
 * The Story and Journal tabs of a conversation.
 *
 * <p><b>Story.</b> Once someone knows you a little (level 1), they bring up what is on their mind
 * and you can offer to help. They ask for something; bring it and they take their time, until
 * you have talked on three different days and reached level 3, when they tell you the rest. Their
 * other two requests can be done any time after the first. Once you have talked on five days,
 * reached level 5 and done both, you answer them one of two ways, and they give you something. A
 * child's story is one request and a gift. The Court counts Favor instead of friendship.
 *
 * <p><b>Journal.</b> The player's own notes on this person: your memories together, what you know
 * about them (personality, the gifts you've found they love or don't), and how their story stands.
 */
final class Storyteller {
    static final int STORY_LEVEL = 1, CONFIDE_VISITS = 3, CONFIDE_LEVEL = 3, END_VISITS = 5, END_LEVEL = 5;

    /** One screen's worth: which tab, what is said (or shown), the status line, the replies. */
    record Page(String tab, String text, String status, List<TalkPayload.Choice> choices) {}

    private Storyteller() {}

    private static TalkPayload.Choice choice(String id, String label, boolean enabled, String hint) {
        return new TalkPayload.Choice(id, label, enabled, hint);
    }

    private static TalkPayload.Choice back() {
        return choice("tab_talk", "Back to talking", true, "");
    }

    private static boolean court(EndFolk folk) {
        return folk instanceof Endarch;
    }

    /** Points for a step of the story: friendship for villagers, Favor (smaller numbers) for the Court. */
    private static int worth(EndFolk folk, int friendship, int favor) {
        return court(folk) ? favor : friendship;
    }

    static String things(Item item, int count) {
        return count + " × " + new ItemStack(item).getHoverName().getString();
    }

    private static String bring(ServerPlayer player, StoryBook.Request r) {
        return "Bring " + things(r.item(), r.count()) + " (you have " + Conversation.count(player, r.item()) + ").";
    }

    private static boolean has(ServerPlayer player, StoryBook.Request r) {
        return player.hasInfiniteMaterials() || Conversation.count(player, r.item()) >= r.count();
    }

    private static TalkPayload.Choice give(ServerPlayer player, int index, StoryBook.Request r) {
        boolean ok = has(player, r);
        return choice("story_give" + index, "Give " + things(r.item(), r.count()), ok, ok ? "" : bring(player, r));
    }

    /** What is still needed for a step: days talked, a level, requests not yet done. */
    private static String need(EndFolk folk, Tale tale, int level, int visits, int minLevel, List<StoryBook.Request> undone) {
        List<String> parts = new ArrayList<>();
        int days = visits - tale.visits;
        if (days > 0) parts.add("talk on " + days + " more " + (days == 1 ? "day" : "days"));
        if (level < minLevel) parts.add("reach " + DialogueBank.get(folk.bank()).levelName(minLevel) + " (" + minLevel + ")");
        if (!undone.isEmpty()) parts.add("help with " + String.join(" and ", undone.stream().map(StoryBook.Request::title).toList()));
        return parts.isEmpty() ? "" : String.join(", ", parts);
    }

    private static List<StoryBook.Request> undoneSides(StoryBook.Story s, Tale tale) {
        return s.requests().stream().skip(1).filter(r -> !tale.done.contains(r.id())).toList();
    }

    private static boolean readyToConfide(Tale tale, int level) {
        return tale.visits >= CONFIDE_VISITS && level >= CONFIDE_LEVEL;
    }

    private static boolean readyToEnd(StoryBook.Story s, Tale tale, int level) {
        return tale.visits >= END_VISITS && level >= END_LEVEL && undoneSides(s, tale).isEmpty();
    }

    // -- the Story tab ------------------------------------------------------------------------------

    static Page story(EndFolk folk, ServerPlayer player, Bond bond, Tale tale) {
        return story(folk, player, bond, tale, null, "");
    }

    /** The Story tab as it stands; {@code said} replaces what they say, {@code gained} leads the status. */
    private static Page story(EndFolk folk, ServerPlayer player, Bond bond, Tale tale, @Nullable String said, String gained) {
        StoryBook.Story s = folk.story();
        int level = folk.meter().level(bond.points);
        Map<String, String> vars = Conversation.vars(folk, player, bond);
        String first = folk.firstName();
        if (s == null) return new Page("story", said != null ? said : folk.lastLine, "No story to tell.", List.of(back()));
        if (tale.chapter == Tale.UNTOLD && level < STORY_LEVEL) {
            return new Page("story", DialogueBank.fill(StoryBook.get(folk.bank()).locked(folk.getRandom()), vars),
                    "Get to know " + first + " better first: reach " + DialogueBank.get(folk.bank()).levelName(STORY_LEVEL)
                            + " (" + STORY_LEVEL + ").", List.of(back()));
        }
        List<TalkPayload.Choice> choices = new ArrayList<>();
        String text, note;
        switch (tale.chapter) {
            case Tale.UNTOLD -> {
                text = s.intro();
                note = first + " has something on their mind.";
                choices.add(choice("story_help", "Offer to help", true, ""));
            }
            case Tale.ASKED -> {
                StoryBook.Request r = s.requests().getFirst();
                text = r.prompt();
                note = bring(player, r);
                choices.add(give(player, 0, r));
            }
            case Tale.HELPED -> {
                boolean ready = readyToConfide(tale, level);
                String needed = need(folk, tale, level, CONFIDE_VISITS, CONFIDE_LEVEL, List.of());
                text = ready ? s.ready() : s.waiting();
                note = ready ? first + " is ready to tell you the rest." : "To hear the rest: " + needed + ".";
                choices.add(choice("story_listen", "I'm listening", ready, ready ? "" : "First " + needed + "."));
                sides(player, s, tale, choices);
            }
            case Tale.CONFIDED -> {
                boolean ready = readyToEnd(s, tale, level);
                String needed = need(folk, tale, level, END_VISITS, END_LEVEL, undoneSides(s, tale));
                text = s.confide();
                note = ready ? "How will you answer " + first + "?" : "Before you answer: " + needed + ".";
                for (int i = 0; i < s.endings().size(); i++) {
                    choices.add(choice("story_end" + i, s.endings().get(i).label(), ready, ready ? "" : "First " + needed + "."));
                }
                sides(player, s, tale, choices);
            }
            default -> {
                text = endingText(s, tale);
                note = "'" + s.title() + "' is told.";
            }
        }
        choices.add(back());
        String status = gained.isEmpty() ? note : gained + " " + note;
        return new Page("story", said != null ? said : DialogueBank.fill(text, vars), status, choices);
    }

    /** The other two requests, open once the first is done. */
    private static void sides(ServerPlayer player, StoryBook.Story s, Tale tale, List<TalkPayload.Choice> choices) {
        for (int i = 1; i < s.requests().size(); i++) {
            StoryBook.Request r = s.requests().get(i);
            if (!tale.done.contains(r.id())) choices.add(choice("story_ask" + i, r.title(), true, "Bring " + things(r.item(), r.count()) + "."));
        }
    }

    private static String endingText(StoryBook.Story s, Tale tale) {
        for (StoryBook.Ending e : s.endings()) if (e.id().equals(tale.ending)) return e.text();
        return s.requests().getFirst().thanks();
    }

    /** Whether the Story tab has something for you to do now (the tab gets a mark). */
    static boolean alert(EndFolk folk, ServerPlayer player, Bond bond, Tale tale) {
        StoryBook.Story s = folk.story();
        int level = folk.meter().level(bond.points);
        if (s == null || level < STORY_LEVEL) return false;
        boolean side = tale.chapter >= Tale.HELPED && tale.chapter < Tale.ENDED
                && s.requests().stream().skip(1).anyMatch(r -> !tale.done.contains(r.id()) && has(player, r));
        return switch (tale.chapter) {
            case Tale.UNTOLD -> true;
            case Tale.ASKED -> has(player, s.requests().getFirst());
            case Tale.HELPED -> side || readyToConfide(tale, level);
            case Tale.CONFIDED -> side || readyToEnd(s, tale, level);
            default -> false;
        };
    }

    /** A story reply; null if it doesn't apply now (a stale button). */
    static @Nullable Page act(EndFolk folk, ServerPlayer player, Bond bond, Tale tale, String action) {
        StoryBook.Story s = folk.story();
        if (s == null) return null;
        int level = folk.meter().level(bond.points);
        long day = folk.dayNumber();
        String first = folk.firstName();
        Map<String, String> vars = Conversation.vars(folk, player, bond);
        if (action.equals("story_help")) {
            if (tale.chapter != Tale.UNTOLD || level < STORY_LEVEL) return null;
            tale.chapter = Tale.ASKED;
            int gain = worth(folk, 3, 1);
            Conversation.gain(folk, bond, gain);
            tale.remember(day, first + " told you about '" + s.title() + "'.");
            return story(folk, player, bond, tale, null, "+" + gain + ".");
        }
        if (action.equals("story_listen")) {
            if (tale.chapter != Tale.HELPED || !readyToConfide(tale, level)) return null;
            tale.chapter = Tale.CONFIDED;
            int gain = worth(folk, 10, 3);
            Conversation.gain(folk, bond, gain);
            tale.remember(day, first + " told you the rest of '" + s.title() + "'.");
            return story(folk, player, bond, tale, null, "+" + gain + ".");
        }
        if (action.startsWith("story_ask") || action.startsWith("story_give")) {
            int i;
            try {
                i = Integer.parseInt(action.substring(action.startsWith("story_ask") ? 9 : 10));
            } catch (NumberFormatException e) {
                return null;
            }
            if (i < 0 || i >= s.requests().size()) return null;
            StoryBook.Request r = s.requests().get(i);
            boolean open = i == 0 ? tale.chapter == Tale.ASKED : tale.chapter >= Tale.HELPED && tale.chapter < Tale.ENDED && !tale.done.contains(r.id());
            if (!open) return null;
            if (action.startsWith("story_ask") || !has(player, r)) {
                List<TalkPayload.Choice> choices = new ArrayList<>(List.of(give(player, i, r)));
                choices.add(i == 0 ? back() : choice("tab_story", "Back to the story", true, ""));
                return new Page("story", DialogueBank.fill(r.prompt(), vars), bring(player, r), choices);
            }
            if (!player.hasInfiniteMaterials()) Conversation.take(player, r.item(), r.count());
            tale.done.add(r.id());
            tale.remember(day, "You brought " + first + " " + things(r.item(), r.count()) + " (" + r.title() + ").");
            int gain = worth(folk, i == 0 ? 15 : 10, i == 0 ? 4 : 3);
            Conversation.gain(folk, bond, gain);
            String said = DialogueBank.fill(r.thanks(), vars);
            if (i == 0) {
                tale.chapter = s.isShort() ? Tale.ENDED : Tale.HELPED;
                if (s.isShort()) return finish(folk, player, bond, tale, s, said, gain);
            }
            return story(folk, player, bond, tale, said, "+" + gain + ".");
        }
        if (action.startsWith("story_end")) {
            int i;
            try {
                i = Integer.parseInt(action.substring(9));
            } catch (NumberFormatException e) {
                return null;
            }
            if (tale.chapter != Tale.CONFIDED || i < 0 || i >= s.endings().size() || !readyToEnd(s, tale, level)) return null;
            StoryBook.Ending e = s.endings().get(i);
            tale.ending = e.id();
            tale.chapter = Tale.ENDED;
            tale.remember(day, DialogueBank.fill(e.memory(), vars));
            return finish(folk, player, bond, tale, s, DialogueBank.fill(e.text(), vars), 0);
        }
        return null;
    }

    /** The end of a story: a last gain of closeness and their gift. */
    private static Page finish(EndFolk folk, ServerPlayer player, Bond bond, Tale tale, StoryBook.Story s, String said, int already) {
        int gain = already + worth(folk, 25, 6);
        Conversation.gain(folk, bond, worth(folk, 25, 6));
        ItemStack gift = new ItemStack(s.gift(), s.giftCount());
        String what = things(s.gift(), s.giftCount());
        if (!gift.isEmpty()) player.getInventory().placeItemBackInInventory(gift, Prediction.SERVER_ONLY);
        tale.remember(folk.dayNumber(), folk.firstName() + " gave you " + what + ".");
        List<TalkPayload.Choice> choices = List.of(back());
        return new Page("story", said, "+" + gain + ". " + folk.firstName() + " gave you " + what + ". '" + s.title() + "' is told.", choices);
    }

    // -- the Journal tab ----------------------------------------------------------------------------

    static Page journal(EndFolk folk, ServerPlayer player, Bond bond, Tale tale, String page) {
        String first = folk.firstName();
        String text = switch (page) {
            case "about" -> about(folk, player, bond, tale);
            case "story" -> notes(folk, bond, tale);
            default -> memories(folk, tale);
        };
        String title = switch (page) {
            case "about" -> "About " + first;
            case "story" -> "Story notes";
            default -> "Memories";
        };
        List<TalkPayload.Choice> choices = List.of(choice("journal_memories", "Memories", true, ""),
                choice("journal_about", "About " + first, true, ""), choice("journal_story", "Story notes", true, ""), back());
        return new Page("journal", text, "Your journal: " + title + ". Scroll to read more.", choices);
    }

    private static String memories(EndFolk folk, Tale tale) {
        StringBuilder out = new StringBuilder("# Memories with " + folk.firstName() + "\n");
        if (tale.memories.isEmpty()) out.append("Nothing written yet. Talk, help, and come back on other days.");
        for (int i = tale.memories.size() - 1; i >= 0; i--) out.append(tale.memories.get(i)).append('\n');
        return out.toString().strip();
    }

    private static String about(EndFolk folk, ServerPlayer player, Bond bond, Tale tale) {
        boolean court = court(folk);
        DialogueBank bank = DialogueBank.get(folk.bank());
        int level = folk.meter().level(bond.points);
        var personality = folk.personality();
        String people = court ? "Endarch of the Court" : folk.people().equals("shulkin") ? folk.isChild() ? "Shulkin child" : "Shulkin"
                : folk.isChild() ? "Chorrin sprout" : "Chorrin";
        StringBuilder out = new StringBuilder("# " + folk.getName().getString() + "\n");
        out.append(people).append(" · ").append(folk.title()).append(" · ").append(folk.settlement().name()).append('\n');
        out.append("Personality: ").append(personality.label()).append(". ").append(personality.about()).append('\n');
        if (court) out.append("Favor with the Court of ").append(folk.settlement().name()).append(": ");
        else out.append("Friendship: ");
        out.append(level).append(" of 10, ").append(bank.levelName(level)).append(" (").append(bond.points).append(court ? " Favor)\n" : " points)\n");
        if (tale.visits > 0) out.append("Talked on ").append(tale.visits).append(tale.visits == 1 ? " day" : " days")
                .append(", first on Day ").append(tale.firstDay + 1).append(".\n");
        for (String taste : List.of("loved", "liked", "disliked")) {
            List<String> items = tale.tastes.entrySet().stream().filter(e -> e.getValue().equals(taste)).map(e -> name(e.getKey())).sorted().toList();
            if (items.isEmpty()) continue;
            String head = switch (taste) {
                case "loved" -> court ? "Esteems: " : "Loves: ";
                case "liked" -> court ? "Accepts: " : "Likes: ";
                default -> court ? "Scorns: " : "Doesn't like: ";
            };
            out.append(head).append(String.join(", ", items)).append('\n');
        }
        if (tale.tastes.isEmpty()) out.append(court ? "Tribute: you haven't learned what the Court esteems.\n" : "Gifts: you haven't found out what they like yet.\n");
        if (!court && bond.grudge > 0) out.append("Still upset with you: you struck them. Say sorry, or give it a day or two.\n");
        return out.toString().strip();
    }

    private static String name(String id) {
        var item = net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse(id));
        return new ItemStack(item).getHoverName().getString();
    }

    private static String notes(EndFolk folk, Bond bond, Tale tale) {
        StoryBook.Story s = folk.story();
        int level = folk.meter().level(bond.points);
        DialogueBank bank = DialogueBank.get(folk.bank());
        if (s == null) return "# Story notes\nThey have no story to tell.";
        if (tale.chapter == Tale.UNTOLD) {
            return "# Story notes\n" + (level < STORY_LEVEL
                    ? "Reach " + bank.levelName(STORY_LEVEL) + " (" + STORY_LEVEL + ") and " + folk.firstName() + " may tell you what is on their mind."
                    : folk.firstName() + " has something on their mind. Ask on the Story tab.");
        }
        String done = "✓ ", todo = "○ ";
        StringBuilder out = new StringBuilder("# " + s.title() + "\n");
        out.append(done).append(folk.firstName()).append(" told you about it.\n");
        StoryBook.Request r0 = s.requests().getFirst();
        out.append(tale.done.contains(r0.id()) ? done : todo).append(r0.title()).append(": ").append(things(r0.item(), r0.count())).append('\n');
        if (!s.isShort()) {
            out.append(tale.chapter >= Tale.CONFIDED ? done : todo).append("Talk on ").append(CONFIDE_VISITS).append(" days and reach ")
                    .append(bank.levelName(CONFIDE_LEVEL)).append(" (").append(CONFIDE_LEVEL).append("): hear the rest.\n");
            for (StoryBook.Request r : s.requests().subList(1, s.requests().size())) {
                out.append(tale.done.contains(r.id()) ? done : todo).append(r.title()).append(": ").append(things(r.item(), r.count())).append('\n');
            }
            out.append(tale.chapter >= Tale.ENDED ? done : todo).append("Talk on ").append(END_VISITS).append(" days, reach ")
                    .append(bank.levelName(END_LEVEL)).append(" (").append(END_LEVEL).append(") and help with both: answer them.\n");
        }
        if (tale.chapter >= Tale.ENDED) {
            String how = s.endings().stream().filter(e -> e.id().equals(tale.ending)).map(StoryBook.Ending::label).findFirst().orElse("");
            out.append(done).append(how.isEmpty() ? "Told." : "You chose: " + how + ".").append(" They gave you ")
                    .append(things(s.gift(), s.giftCount())).append(".\n");
        }
        out.append("Days talked: ").append(tale.visits).append('.');
        return out.toString();
    }
}
