import json

skills = ["agentic","ant","artistic","basic","bento","bold","brutalism","cafe","claude",
"claymorphism","clean","codex","colorful","contemporary","corporate","cosmic","creative",
"dithered","doodle","dramatic","editorial","enterprise","expressive","fantasy","fiction",
"flat","friendly","futuristic","geometric","glassmorphism","gradient","immersive",
"impeccable","levels","lingo","material","matrix","minimal","modern","mono","neobrutalism",
"neon","neumorphism","pacman","paper","perspective","power","premium","professional",
"pulse","refined","retro","riso","roku","sega","shadcn","sketch","skeumorphism","sleek",
"spacious","square","stitch","storytelling","terracotta","tetris","vibrant","vintage"]

assert len(skills) == 67, len(skills)

lines = []
for s in skills:
    lines.append({
        "category": "nl_quality",
        "rule_id": "R01",
        "file": "skills/" + s + "/SKILL.md",
        "line": None,
        "severity": "low",
        "confidence": "high",
        "evidence": "grep for the R01 penalized-term list matched \"as relevant\" in the line: \"- Define required states: default, hover, focus-visible, active, disabled, loading, error (as relevant).\"",
        "penalty": -2,
        "pattern": "as relevant",
        "description": "Vague quantifier \"as relevant\" used without a measurable criterion, in the Component Rule Expectations list",
        "false_positive": False,
        "suggested_fix": "Replace \"(as relevant)\" with an explicit rule for which states are required per component type, or remove the qualifier"
    })

empty_brand = ["artistic","bold","editorial","futuristic","geometric","minimal","neobrutalism","power","retro","square"]
for s in empty_brand:
    lines.append({
        "category": "cross_component",
        "rule_id": "CC-incomplete-section",
        "file": "skills/" + s + "/SKILL.md",
        "line": None,
        "severity": "low",
        "confidence": "high",
        "evidence": "\"## Brand\" header is immediately followed by \"## Style Foundations\" with no text in between",
        "penalty": None,
        "pattern": "## Brand followed directly by ## Style Foundations",
        "description": "Brand section is body-empty, contradicting README's documented required content (Brand & mission) for SKILL.md files",
        "false_positive": False,
        "suggested_fix": "Add a brand narrative paragraph matching the pattern used in the other 57 skills"
    })

lines.append({
    "category": "cross_component",
    "rule_id": "CC-orphan-component",
    "file": "registry-examples/",
    "line": None,
    "severity": "low",
    "confidence": "low",
    "evidence": "",
    "penalty": None,
    "pattern": "anime|candy|dark|forest|machine|mars|matcha|minimax|nostalgia|pragmatic",
    "description": "10 marketing images (anime, candy, dark, forest, machine, mars, matcha, minimax, nostalgia, pragmatic) have no corresponding skills directory, index.json entry, or README reference",
    "false_positive": False,
    "suggested_fix": "Remove unused images or add the corresponding skills if they are planned"
})

out_path = "/home/runner/work/nlpm/nlpm/auditor/audits/bergside-awesome-design-skills.findings.jsonl"
with open(out_path, "w") as f:
    for obj in lines:
        f.write(json.dumps(obj) + "\n")

print("wrote", len(lines), "lines")
