import { PrismaClient } from "@prisma/client";
import * as fs from "fs";
import * as path from "path";

const prisma = new PrismaClient();

interface ScenarioJson {
  id: string;
  name: string;
  description: string;
  demographics: string;
  presenting_issue: string;
  ambivalence: {
    change: string[];
    status_quo: string[];
  };
  resistance_level: number;
  background: string;
  personality_notes: string;
  potential_change_talk_triggers: string[];
  common_sustain_talk: string[];
  opening_statement: string;
}

async function main() {
  const scenariosDir = path.join(__dirname, "../../mi_trainer/scenarios");
  const files = fs.readdirSync(scenariosDir).filter((f) => f.endsWith(".json"));

  console.log(`Found ${files.length} scenario files`);

  for (const file of files) {
    const filePath = path.join(scenariosDir, file);
    const content = fs.readFileSync(filePath, "utf-8");
    const data: ScenarioJson = JSON.parse(content);

    const scenario = await prisma.scenario.upsert({
      where: { slug: data.id },
      update: {
        name: data.name,
        description: data.description,
        demographics: data.demographics,
        presentingIssue: data.presenting_issue,
        ambivalence: {
          change: data.ambivalence.change,
          statusQuo: data.ambivalence.status_quo,
        },
        resistanceLevel: data.resistance_level,
        background: data.background,
        personalityNotes: data.personality_notes,
        changeTalkTriggers: data.potential_change_talk_triggers,
        sustainTalk: data.common_sustain_talk,
        openingStatement: data.opening_statement,
        isBuiltin: true,
      },
      create: {
        slug: data.id,
        name: data.name,
        description: data.description,
        demographics: data.demographics,
        presentingIssue: data.presenting_issue,
        ambivalence: {
          change: data.ambivalence.change,
          statusQuo: data.ambivalence.status_quo,
        },
        resistanceLevel: data.resistance_level,
        background: data.background,
        personalityNotes: data.personality_notes,
        changeTalkTriggers: data.potential_change_talk_triggers,
        sustainTalk: data.common_sustain_talk,
        openingStatement: data.opening_statement,
        isBuiltin: true,
      },
    });

    console.log(`Seeded scenario: ${scenario.name}`);
  }

  console.log("Seeding complete!");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
