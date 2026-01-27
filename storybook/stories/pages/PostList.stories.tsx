import type { Meta, StoryObj } from "@storybook/react";
import { PostList } from "@/components/pages/post-list";

const meta = {
  title: "Pages/PostList",
  component: PostList,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof PostList>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
