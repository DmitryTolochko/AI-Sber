import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { AlternativeTranslationsStore } from "@/utils/interfaces";

/**
 * Хук для хранения альтернативных переводов
 */
const useAlternativeTranslationsStore = create<AlternativeTranslationsStore>()(
  persist(
    (set, get) => ({
      alternativeTranslations: [],
      addAlternativeTranslation: (translation) =>
        set({
          alternativeTranslations: [
            ...get().alternativeTranslations,
            translation,
          ],
        }),
      clearAlternativeTranslations: () => set({ alternativeTranslations: [] }),
    }),
    {
      name: "alternative-translations-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useAlternativeTranslationsStore;
