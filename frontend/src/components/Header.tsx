/* eslint-disable react-hooks/exhaustive-deps */
"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import Button from "./ui/Button";
import useNavigationStore from "@/hooks/useNavigationStore";
import useLocalStorage from "@/hooks/useLocalStorage";

export default function Header() {
  const router = useRouter();
  const { navigationTab, setNavigationTab } = useNavigationStore();
  const { setValue } = useLocalStorage();

  useEffect(() => {
    router.push(`/${navigationTab}`);
    setValue("lastNavigationTab", navigationTab);
  }, [navigationTab]);

  return (
    <header className="w-full py-5 flex justify-between items-center">
      <div className="text-3xl">Переводчик</div>
      <div className="flex gap-2">
        <Button
          active={navigationTab === "translator"}
          onClick={() => setNavigationTab("translator")}
        >
          Переводчик
        </Button>
        <Button
          active={navigationTab === "favorites"}
          onClick={() => setNavigationTab("favorites")}
        >
          Избранные переводы
        </Button>
        <Button
          active={navigationTab === "history"}
          onClick={() => setNavigationTab("history")}
        >
          История
        </Button>
      </div>
    </header>
  );
}
