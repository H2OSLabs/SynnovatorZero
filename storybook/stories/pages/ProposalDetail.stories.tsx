import type { Meta, StoryObj } from "@storybook/react";
import { ProposalDetail } from "@/components/pages/proposal-detail";

const meta = {
  title: "Pages/ProposalDetail",
  component: ProposalDetail,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof ProposalDetail>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
