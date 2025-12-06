import React from "react";
import { motion, AnimatePresence } from "motion/react";
import TextArea from "../ui/TextArea";

export default function TranslationExamples({
  alternativeTranslations,
}: {
  alternativeTranslations: string[];
}) {
  function onAddToFavorites() {}
  function onRemoveFromFavorites() {}

  return (
    <AnimatePresence mode="wait">
      {alternativeTranslations.length > 0 && (
        <motion.div
          key="translation-examples"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="w-full  px-[10.417vw] pt-[1.146vw] pb-[4.219vw] mt-[1.927vw] bg-[#D9E4D9]"
        >
          <h2 className="text-[1.667vw] text-[#2C734E] mb-[0.972vw] font-semibold">
            Варианты перевода
          </h2>

          <ul className="flex flex-col gap-[0.625vw]">
            {alternativeTranslations
              .reverse()
              .map((sentence: string, index: number) => (
                <li key={index} className="bg-white rounded-[0.625vw]">
                  <TextArea
                    value={sentence}
                    className="border-none text-[1.667vw]"
                    copy
                    tts
                    interactive={false}
                    disabled
                    onAddToFavorites={onAddToFavorites}
                    onRemoveFromFavorites={onRemoveFromFavorites}
                  />
                </li>
              ))}
          </ul>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
