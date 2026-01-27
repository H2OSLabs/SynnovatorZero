import type { Meta, StoryObj } from "@storybook/react";
import { ProposalList } from "@/components/pages/proposal-list";

const meta = {
  title: "Pages/ProposalList",
  component: ProposalList,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof ProposalList>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
