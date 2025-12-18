import TextArea from "@/components/ui/TextArea";
import { HistoryItemProps } from "@/utils/interfaces";

const HistoryItem = ({
  sourceLanguage,
  content,
  onDelete,
}: HistoryItemProps) => {
  return (
    <div className="w-full border-[1px] border-[#B8B8B8] pt-[1.111vw] rounded-[1.111vw] relative">
      <span className="px-[1.111vw] text-[#2C734E] text-[1.111vw] flex items-center justify-between">
        {sourceLanguage === "nanai" ? "Нанайский" : "Русский"}
        {onDelete && (
          <button
            onClick={onDelete}
            className="text-red-600 hover:text-red-800 text-[1.111vw] font-semibold"
            aria-label="Удалить из истории"
          >
            ✕
          </button>
        )}
      </span>
      <TextArea
        value={content}
        className="border-none text-[1.667vw]"
        copy
        tts
        interactive={false}
        disabled
      />
    </div>
  );
};

export default HistoryItem;
