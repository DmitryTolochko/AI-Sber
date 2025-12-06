"use client";
import TranslationExamples from "@/components/translator/TranslationExamples";
import LanguageSwitcher from "../../components/translator/LangaugeSwitcher";
import TranslationArea from "../../components/translator/TranslationArea";
import useTranslationStore from "@/hooks/useTranslationStore";
import useAlternativeTranslationsStore from "@/hooks/useAlternativeTranslationsStore";
import UsageExamples from "@/components/translator/UsageExamples";
import useUsagesStore from "@/hooks/useUsagesStore";

export default function Translator() {
  const { alternativeTranslations } = useAlternativeTranslationsStore();
  const { translateTo, setTranslateTo } = useTranslationStore();
  const { wordUsages, sentencesUsages } = useUsagesStore();
  const handleLanguageChange = (lang: "nanai" | "russian") => {
    setTranslateTo(lang);
  };

  return (
    <div className="pt-[4.167vw]">
      <h1 className="text-[1.667vw] text-[#2C734E] mb-[0.972vw] font-semibold">
        Нанайско-русский онлайн переводчик
      </h1>
      <LanguageSwitcher
        activeTargetLanguage={translateTo}
        onChange={handleLanguageChange}
      />
      <TranslationArea />

      <div className="w-[calc(100%+10.417vw*2)] -mx-[10.417vw]">
        <TranslationExamples
          alternativeTranslations={alternativeTranslations}
        />
        <UsageExamples
          wordUsages={wordUsages}
          sentencesUsages={sentencesUsages}
        />
      </div>
    </div>
  );
}
