"""Single source for the site's FAQ, its FAQPage structured data, llms.txt, and llms-full.txt.

Edit FAQ below, then run from the repository root:

    python3 scripts/build-faq.py . path/to/obsidian-section-meter/README.md

The README is included in llms-full.txt.
"""
import html
import json
import re
import sys

SITE = "https://martinowong.github.io/section-writing-stats-site/"
REPO = "https://github.com/martinowong/obsidian-section-meter"
INSTALL = "https://community.obsidian.md/plugins/section-meter"

# (question, answer). Answers may use `code`; it becomes <code> on the page.
FAQ = [
    ("What does Section Writing Stats do?",
     "It shows live word counts, character counts, and reading-time estimates beside every Markdown heading, below the note title, and in the status bar, and it tracks writing targets for a whole note or a single section."),
    ("What counts as a section?",
     "A heading includes everything beneath it, including nested headings, until the next heading at the same or a higher level. A chapter's count therefore includes all of its scenes."),
    ("How do I set a writing target?",
     "Put the cursor in a section and run Set or edit current-section writing target from the command palette, or type a line such as `Target: 750 words` below the heading yourself. A target above the first heading applies to the whole note."),
    ("Which target formats work?",
     "Words, characters, or reading time: `Target: 250 words`, `target 250w`, `Target: 1800 chars`, `Target: 3m`, `Target: 2m 30s`, or `Target: 45s`. The line must stand on its own and include a unit, and `Target` is case-insensitive."),
    ("Can a section have its own target inside a larger one?",
     "Yes. A parent heading's target covers all of its subsections, and a nested heading can define its own target, which takes priority while you write in that subsection."),
    ("Are targets managed in a separate file?",
     "No. A target is an ordinary line in the note itself, such as `Target: 750 words`, so it travels with the note and stays readable without the plugin. In Live Preview it shows as a small chip; click it to edit the text, or turn chips off in settings."),
    ("What is excluded from the counts?",
     "YAML frontmatter, fenced and inline code, embeds, comments, HTML, and the target lines themselves. Text in paragraphs, lists, blockquotes, links, and table cells is counted."),
    ("How is reading time estimated?",
     "From the word count and a reading speed you choose in settings, from 100 to 500 words per minute. The default is 200."),
    ("Can I choose where the statistics appear?",
     "Yes. Show them beside headings, below the note title, in the status bar, or any combination, and pick words, reading time, or characters separately for badges and the status bar."),
    ("Does it work in Reading view?",
     "Yes. Heading and title badges appear in both the editor and Reading view, using the same settings."),
    ("Does it work on mobile?",
     "Yes. It runs on Obsidian for iOS and Android, and an optional sticky meter shows the current target's progress while you scroll."),
    ("Can it count selected text?",
     "Yes. Select any passage and the status bar shows its words, characters, and reading time."),
    ("Will it slow down long notes?",
     "It is built for long manuscripts: counts update after a short pause in typing, and only headings on screen get badges. A 55,000-word note with 480 headings recounts in under 10 milliseconds on a Mac."),
    ("Does it collect data or need the internet?",
     "No. The plugin makes no network requests and keeps everything on your device."),
    ("How is it different from Obsidian's built-in word count?",
     "Obsidian's word count shows totals for the whole note or a selection. Section Writing Stats adds counts for every heading, reading time, and writing targets with progress."),
    ("Which headings are supported?",
     "Headings written with `#` marks, from `#` to `######`. Underline-style (Setext) headings are not supported."),
    ("Is it free?",
     "Yes. It is free and open source under the MIT License. If it helps your writing, you can leave a tip."),
]


def page_answer(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text, quote=False))


def plain_answer(text: str) -> str:
    return text.replace("`", "")


def faq_html() -> str:
    items = "\n".join(
        f"""          <details>
            <summary>{html.escape(q, quote=False)}</summary>
            <p>{page_answer(a)}</p>
          </details>"""
        for q, a in FAQ
    )
    return f"""      <section class="faq-section" id="faq" aria-labelledby="faq-title">
        <div class="faq-heading reveal">
          <h2 id="faq-title">FAQ</h2>
        </div>
        <div class="faq-list reveal">
{items}
        </div>
      </section>"""


def faq_json_ld() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain_answer(a)}}
            for q, a in FAQ
        ],
    }
    body = json.dumps(data, indent=2, ensure_ascii=False)
    return '    <script type="application/ld+json" id="faq-structured-data">\n' + "\n".join(
        "      " + line for line in body.split("\n")) + "\n    </script>"


def faq_markdown() -> str:
    return "\n\n".join(f"### {q}\n\n{a}" for q, a in FAQ)


LLMS_HEADER = f"""# Section Writing Stats

> Section Writing Stats is a free, open-source Obsidian community plugin that shows live word counts, character counts, reading-time estimates, and writing-target progress for every Markdown heading section, the whole note, and selected text.

A section includes its nested subheadings until the next heading of the same or a higher level. Writing targets are ordinary Markdown lines such as `Target: 750 words`, so notes stay portable. The plugin works on desktop and mobile, needs Obsidian 1.13 or later, and makes no network requests.

## Key features

- Live statistics beside Markdown headings, below the note title, and in the status bar, in both the editor and Reading view.
- Word counts, character counts (with or without spaces), and reading-time estimates at an adjustable reading speed.
- Writing targets in words, characters, or reading time for a whole note or any section, with progress labels as a count, percentage, or amount remaining.
- Target lines shown as editable chips in Live Preview; progress turns green with a check when a target is reached.
- Selected-text statistics, compact labels, hiding of short sections, command-palette toggles, and an optional sticky target meter on mobile.

## Links

- [Install in Obsidian]({INSTALL}): Obsidian Community Plugins page.
- [Website]({SITE}): overview and an interactive example.
- [Source code and documentation]({REPO}): README, writing-target guide, and issue tracker.
- [Release notes]({REPO}/releases): what changed in each version.
- [Full documentation for LLMs]({SITE}llms-full.txt): this file plus the complete README.

## Publisher

Created and maintained by Martino Wong, released under the MIT License.
"""


def main() -> None:
    site, readme_path = sys.argv[1], sys.argv[2]

    page = open(f"{site}/index.html").read()
    start = page.index('      <section class="faq-section"')
    end = page.index("</section>", start) + len("</section>")
    page = page[:start] + faq_html() + page[end:]

    marker = '    <script type="application/ld+json" id="faq-structured-data">'
    if marker in page:
        start = page.index(marker)
        end = page.index("</script>", start) + len("</script>")
        page = page[:start] + faq_json_ld() + page[end:]
    else:
        page = page.replace("  </head>", faq_json_ld() + "\n  </head>", 1)
    open(f"{site}/index.html", "w").write(page)

    open(f"{site}/llms.txt", "w").write(LLMS_HEADER + "\n## Frequently asked questions\n\n" + faq_markdown() + "\n")

    readme = open(readme_path).read()
    # Drop the README's images; they mean nothing in plain text.
    readme = re.sub(r"^!\[[^\]]*\]\([^)]*\)\n\n?", "", readme, flags=re.M)
    # Nest the README under its own heading by moving every heading down a level.
    in_code = False
    lines = []
    for line in readme.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        lines.append("#" + line if line.startswith("#") and not in_code else line)
    open(f"{site}/llms-full.txt", "w").write(
        LLMS_HEADER + "\n## Frequently asked questions\n\n" + faq_markdown()
        + "\n\n## Full documentation (plugin README)\n\n" + "\n".join(lines).lstrip("\n"))


if __name__ == "__main__":
    main()
