import type { Meta, StoryObj } from "@storybook/react";
import { PostDetail } from "@/components/pages/post-detail";

const meta = {
  title: "Pages/PostDetail",
  component: PostDetail,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof PostDetail>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
