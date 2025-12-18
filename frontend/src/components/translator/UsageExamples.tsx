import ChatIcon from "@/icons/ChatIcon";
import DictionaryIcon from "@/icons/DictionaryIcon";
import React from "react";
import { motion, AnimatePresence } from "motion/react";

export default function UsageExamples({
  wordUsages,
  sentencesUsages,
}: {
  wordUsages: string[];
  sentencesUsages: { original: string; translation: string }[];
}) {
  return (
    <AnimatePresence mode="wait">
      {(wordUsages.length > 0 || sentencesUsages.length > 0) && (
        <motion.div
          key="usage-examples"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.4, ease: "easeOut", delay: 0.2 }}
          className="px-[10.417vw] pt-[1.146vw] pb-[4.219vw] mt-[1.927vw] bg-[#D9E4D9]"
        >
          <div className="flex justify-between items-start bg-white rounded-[0.625vw] p-[1.042vw]">
            <div className="w-full text-[1.667vw] text-[#2C734E] mb-[0.972vw] font-semibold">
              <h2 className="pb-[0.625vw]">Примеры использования</h2>
              <ul className="flex flex-col gap-[1.667vw]">
                {sentencesUsages.slice(0, 5).map((usage, index) => (
                  <li key={index}>
                    <div className="text-black font-normal flex gap-[0.833vw]">
                      <div className="size-[1.875vw]">
                        <ChatIcon />
                      </div>
                      <div className="text-[0.833vw] flex flex-col max-w-[80%]">
                        <p>{usage.original}</p>
                        <p className="text-[#868686]">{usage.translation}</p>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            <div className="w-full text-[1.667vw] text-[#2C734E] mb-[0.972vw] font-semibold">
              <h2 className="pb-[0.625vw]">Словарь</h2>
              <ul className="flex flex-col gap-[1.667vw]">
                {wordUsages.slice(0, 5).map((word, index) => (
                  <li key={index}>
                    <div className="text-black font-normal flex items-center gap-[0.833vw]">
                      <div className="size-[1.875vw]">
                        <DictionaryIcon />
                      </div>
                      <div className="text-[0.833vw] flex flex-col max-w-[80%]">
                        <p>{word}</p>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
