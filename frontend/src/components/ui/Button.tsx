import React from "react";
import clsx from "clsx";

interface ButtonProps {
  children?: React.ReactNode;
  onClick: () => void;
  className?: string;
  active?: boolean;
  disabled?: boolean;
}

export default function Button({
  children,
  onClick,
  className,
  active,
  disabled,
}: ButtonProps) {
  return (
    <button
      disabled={disabled}
      onClick={onClick}
      className={clsx(
        "flex w-fit py-2 px-4 hover:cursor-pointer",
        active ? "bg-red-500" : "bg-blue-500",
        className
      )}
    >
      {children}
    </button>
  );
}
