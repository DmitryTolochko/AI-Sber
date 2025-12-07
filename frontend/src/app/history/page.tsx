"use client";

import useHistoryStore from "@/hooks/useHistoryStore";
import HistoryItem from "../../components/history/HistoryItem";

export default function History() {
  const { historyTranslations, removeHistoryTranslation } = useHistoryStore();

  return (
    <div className="pt-[4.167vw]">
      <h1 className="text-[1.667vw] text-[#2C734E] mb-[0.972vw] font-semibold">
        История переводов
      </h1>
      <div className="w-full flex flex-col-reverse gap-[1.389vw]">
        {historyTranslations.length === 0 ? (
          <p className="text-[1.111vw] text-gray-500">
            История переводов пуста
          </p>
        ) : (
          historyTranslations.map((item) => {
            return (
              <div key={item.id} className="flex flex-col gap-[0.694vw]">
                <div className="flex gap-[1.389vw]">
                  <HistoryItem
                    sourceLanguage={item.sourceLanguage}
                    content={item.sourceText}
                  />
                  <HistoryItem
                    sourceLanguage={item.targetLanguage}
                    content={item.targetText}
                  />
                </div>
                <div className="flex justify-between items-center px-[0.5vw]">
                  <span className="text-[0.972vw] text-gray-500">
                    {new Date(item.translatedAt).toLocaleString("ru-RU", {
                      day: "2-digit",
                      month: "2-digit",
                      year: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                  <button
                    onClick={() => removeHistoryTranslation(item.id)}
                    className="text-red-600 hover:text-red-800 text-[0.972vw] font-semibold px-[0.694vw] py-[0.347vw] hover:bg-red-50 rounded transition-colors"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
