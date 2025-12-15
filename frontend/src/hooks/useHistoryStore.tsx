import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { HistoryTranslationItem, HistoryStore } from "@/utils/interfaces";

/**
 * Хук для хранения истории переводов
 */
const useHistoryStore = create<HistoryStore>()(
  persist(
    (set, get) => ({
      historyTranslations: [],
      addHistoryTranslation: (translation) =>
        set({
          historyTranslations: [...get().historyTranslations, translation],
        }),
      removeHistoryTranslation: (id: HistoryTranslationItem["id"]) =>
        set({
          historyTranslations: get().historyTranslations.filter(
            (t) => t.id !== id
          ),
        }),
    }),
    {
      name: "history-translations-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useHistoryStore;
