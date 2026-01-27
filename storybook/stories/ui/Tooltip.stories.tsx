import type { Meta, StoryObj } from "@storybook/react";
import { Info, HelpCircle } from "lucide-react";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";

const meta = {
  title: "UI/Tooltip",
  component: Tooltip,
  tags: ["autodocs"],
} satisfies Meta<typeof Tooltip>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button variant="outline">Hover me</Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>This is a tooltip</p>
      </TooltipContent>
    </Tooltip>
  ),
};

export const WithIcon: Story = {
  render: () => (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button variant="ghost" size="icon">
          <Info />
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>More information</p>
      </TooltipContent>
    </Tooltip>
  ),
};

export const Positions: Story = {
  name: "All Positions",
  render: () => (
    <div className="flex gap-8 items-center p-8">
      <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="outline" size="sm">Top</Button>
        </TooltipTrigger>
        <TooltipContent side="top">
          <p>Top tooltip</p>
        </TooltipContent>
      </Tooltip>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="outline" size="sm">Bottom</Button>
        </TooltipTrigger>
        <TooltipContent side="bottom">
          <p>Bottom tooltip</p>
        </TooltipContent>
      </Tooltip>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="outline" size="sm">Left</Button>
        </TooltipTrigger>
        <TooltipContent side="left">
          <p>Left tooltip</p>
        </TooltipContent>
      </Tooltip>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="outline" size="sm">Right</Button>
        </TooltipTrigger>
        <TooltipContent side="right">
          <p>Right tooltip</p>
        </TooltipContent>
      </Tooltip>
    </div>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full">
          <HelpCircle className="w-4 h-4" />
          帮助
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>点击获取帮助信息</p>
      </TooltipContent>
    </Tooltip>
  ),
};
