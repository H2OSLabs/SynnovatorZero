import type { Meta, StoryObj } from "@storybook/react";
import { Team } from "@/components/pages/team";

const meta = {
  title: "Pages/Team",
  component: Team,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof Team>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
