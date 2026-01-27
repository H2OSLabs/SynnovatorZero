import type { Meta, StoryObj } from "@storybook/react";
import { UserProfile } from "@/components/pages/user-profile";

const meta = {
  title: "Pages/UserProfile",
  component: UserProfile,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof UserProfile>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
