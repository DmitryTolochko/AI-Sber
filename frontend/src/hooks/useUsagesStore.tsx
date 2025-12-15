import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { UsagesStore } from "@/utils/interfaces";

/**
 * Хук для хранения использований слов
 */
const useUsagesStore = create<UsagesStore>()(
  persist(
    (set, get) => ({
      wordUsages: [],
      sentencesUsages: [],
      setWordUsages: (words) => set({ wordUsages: words }),
      setSentencesUsages: (sentences) => set({ sentencesUsages: sentences }),
      clearUsages: () => set({ wordUsages: [], sentencesUsages: [] }),
    }),
    {
      name: "usages-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useUsagesStore;
