import type { Meta, StoryObj } from "@storybook/react";
import { Assets } from "@/components/pages/assets";

const meta = {
  title: "Pages/Assets",
  component: Assets,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof Assets>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
