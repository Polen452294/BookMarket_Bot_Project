import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig(({ mode }) => {
  // читаем env из ../ (корень монорепы)
  const env = loadEnv(mode, path.resolve(__dirname, ".."), "VITE_");

  return {
    plugins: [react()],
    // важно: не трогаем define import.meta.env целиком
    envDir: path.resolve(__dirname, ".."),
  };
});
