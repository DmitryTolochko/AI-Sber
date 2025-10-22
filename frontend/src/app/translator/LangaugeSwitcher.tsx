import Button from "@/components/ui/Button";

interface LanguageSwitcherProps {
  activeTargetLanguage: "nanai" | "russian";
  onChange: () => void;
}

const LanguageSwitcher = ({
  activeTargetLanguage,
  onChange,
}: LanguageSwitcherProps) => {
  return (
    <div className="flex justify-between gap-5">
      <div className="w-full flex justify-center items-center bg-gray-400">
        {activeTargetLanguage === "nanai" ? "Русский" : "Нанайский"}
      </div>
      <Button onClick={onChange}>Switch</Button>
      <div className="w-full flex justify-center items-center  bg-gray-400">
        {activeTargetLanguage === "nanai" ? "Нанайский" : "Русский"}
      </div>
    </div>
  );
};

export default LanguageSwitcher;
