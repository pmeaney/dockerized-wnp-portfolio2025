import { Nunito } from "next/font/google";

export const nunito = Nunito({
  weight: "500",
  subsets: ["latin"],
  display: "swap", // Show system font immediately (see FOUT (Flash of Unstyled Text)), swap to custom font when ready
  preload: true, // tells the browser "this font is critical - I want you to start downloading it as soon as possible."
});

export const nunitoBold = Nunito({
  weight: "900",
  subsets: ["latin"],
  display: "swap", // Show system font immediately (see FOUT (Flash of Unstyled Text)), swap to custom font when ready
  preload: true, // tells the browser "this font is critical - I want you to start downloading it as soon as possible."
});

export const nunitoSemiBold = Nunito({
  weight: "700",
  subsets: ["latin"],
  display: "swap", // Show system font immediately (see FOUT (Flash of Unstyled Text)), swap to custom font when ready
  preload: true, // tells the browser "this font is critical - I want you to start downloading it as soon as possible."
});
