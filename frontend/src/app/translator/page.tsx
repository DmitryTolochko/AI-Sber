"use client";
import { useState } from "react";
import LanguageSwitcher from "./LangaugeSwitcher";
import TranslationArea from "./TranslationArea";
import useLocalStorage from "@/hooks/useLocalStorage";

export default function Translator() {
  const { setValue, getValue } = useLocalStorage();

  // Мб создать отдельный useTranslationStore для всей логики
  const [targetLanguage, setTargetLanguage] = useState<"nanai" | "russian">(
    (getValue("lastTargetLanguage") as "nanai" | "russian") || "russian"
  );

  const handleTargetLanguageSwitch = () => {
    const updatedValue = targetLanguage === "russian" ? "nanai" : "russian";
    setTargetLanguage(updatedValue);
    setValue("lastTargetLanguage", updatedValue);
  };

  return (
    <div className="pt-10">
      <LanguageSwitcher
        activeTargetLanguage={targetLanguage}
        onChange={handleTargetLanguageSwitch}
      />
      <TranslationArea />
    </div>
  );
}
