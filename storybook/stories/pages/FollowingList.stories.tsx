import type { Meta, StoryObj } from "@storybook/react";
import { FollowingList } from "@/components/pages/following-list";

const meta = {
  title: "Pages/FollowingList",
  component: FollowingList,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof FollowingList>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
