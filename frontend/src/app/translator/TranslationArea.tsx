import TextArea from "@/components/ui/TextArea";
import React, { useEffect, useState } from "react";
import useDebouncedValue from "@/hooks/useDebouncedValue";

export default function TranslationArea() {
  const [originalText, setOriginalText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [height1, setHeight1] = useState<number>(0);
  const [height2, setHeight2] = useState<number>(0);
  const syncHeight = Math.max(height1, height2);

  const debouncedOriginal = useDebouncedValue(originalText, 500) as string;

  useEffect(() => {
    if (debouncedOriginal === "") {
      setTranslatedText("");
      return;
    }

    setTranslatedText("Уже переводим...");
    const api = setTimeout(() => {
      setTranslatedText(`[Типо перевод] ${debouncedOriginal} [Типо перевод]`);
    }, 1200);

    return () => {
      clearTimeout(api);
    };
  }, [debouncedOriginal]);

  return (
    <div className="grid grid-cols-2 mt-5 gap-5 items-stretch">
      <TextArea
        value={originalText}
        onChange={setOriginalText}
        placeholder="Начните вводить текст..."
        maxLength={200}
        syncHeight={syncHeight}
        onHeightChange={setHeight1}
        className="bg-gray-100"
      />
      <TextArea
        placeholder="Здесь появится перевод..."
        value={translatedText}
        disabled
        syncHeight={syncHeight}
        onHeightChange={setHeight2}
      />
    </div>
  );
}
