import type { Meta, StoryObj } from "@storybook/react";
import { CategoryDetail } from "@/components/pages/category-detail";

const meta = {
  title: "Pages/CategoryDetail",
  component: CategoryDetail,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof CategoryDetail>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
