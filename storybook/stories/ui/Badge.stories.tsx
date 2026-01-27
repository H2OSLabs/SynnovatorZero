import type { Meta, StoryObj } from "@storybook/react";
import { Zap, Star, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const meta = {
  title: "UI/Badge",
  component: Badge,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "secondary", "destructive", "outline", "ghost", "link"],
    },
  },
} satisfies Meta<typeof Badge>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Badge",
    variant: "default",
  },
};

export const Secondary: Story = {
  args: {
    children: "Secondary",
    variant: "secondary",
  },
};

export const Destructive: Story = {
  args: {
    children: "Destructive",
    variant: "destructive",
  },
};

export const Outline: Story = {
  args: {
    children: "Outline",
    variant: "outline",
  },
};

export const Ghost: Story = {
  args: {
    children: "Ghost",
    variant: "ghost",
  },
};

export const LinkBadge: Story = {
  name: "Link",
  args: {
    children: "Link",
    variant: "link",
  },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <Star /> Featured
      </>
    ),
  },
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <div className="flex flex-wrap gap-3">
      <Badge className="bg-[var(--nf-lime)] text-[var(--nf-surface)] rounded-full px-4 py-1.5 text-[13px] font-semibold">
        热门
      </Badge>
      <Badge className="bg-[var(--nf-blue)] text-white rounded-full px-3 py-1">
        <Zap className="w-3 h-3" /> 精选
      </Badge>
      <Badge className="bg-[var(--nf-orange)] text-white rounded-full px-3 py-1">
        <AlertCircle className="w-3 h-3" /> 新品
      </Badge>
      <Badge className="bg-[var(--nf-cyan)] text-[var(--nf-surface)] rounded-full px-3 py-1">
        科技
      </Badge>
      <Badge className="bg-[var(--nf-pink)] text-[var(--nf-surface)] rounded-full px-3 py-1">
        设计
      </Badge>
    </div>
  ),
};

export const AllVariants: Story = {
  name: "All Variants",
  render: () => (
    <div className="flex flex-wrap gap-3">
      <Badge variant="default">Default</Badge>
      <Badge variant="secondary">Secondary</Badge>
      <Badge variant="destructive">Destructive</Badge>
      <Badge variant="outline">Outline</Badge>
      <Badge variant="ghost">Ghost</Badge>
      <Badge variant="link">Link</Badge>
    </div>
  ),
};
