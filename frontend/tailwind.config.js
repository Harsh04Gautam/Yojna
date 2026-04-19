/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        plusjakartasans: ["PlusJakartaSans-Regular", "sans-serif"],
        "plusjakartasans-bold": ["PlusJakartaSans-Bold", "sans-serif"],
        "plusjakartasans-extrabold": [
          "PlusJakartaSans-ExtraBold",
          "sans-serif",
        ],
        "plusjakartasans-medium": ["PlusJakartaSans-Medium", "sans-serif"],
        "plusjakartasans-light": ["PlusJakartaSans-Light", "sans-serif"],
      },
    },
  },
  plugins: [],
};
