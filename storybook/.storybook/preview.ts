import type { Preview, Decorator } from "@storybook/react";
import { withThemeByClassName } from "@storybook/addon-themes";
import "../app.css";

const withDarkWrapper: Decorator = (Story) => {
  return Story();
};

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: "neon-forge-dark",
      values: [
        { name: "neon-forge-dark", value: "#181818" },
        { name: "surface", value: "#00000E" },
        { name: "card", value: "#222222" },
        { name: "white", value: "#FFFFFF" },
      ],
    },
    layout: "centered",
  },
  decorators: [
    withDarkWrapper,
    withThemeByClassName({
      themes: {
        light: "",
        dark: "dark",
      },
      defaultTheme: "dark",
    }),
  ],
};

export default preview;
