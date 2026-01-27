import type { Meta, StoryObj } from "@storybook/react";
import { Zap, Download, Trash2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const meta = {
  title: "UI/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "destructive", "outline", "secondary", "ghost", "link"],
    },
    size: {
      control: "select",
      options: ["default", "xs", "sm", "lg", "icon", "icon-xs", "icon-sm", "icon-lg"],
    },
    disabled: { control: "boolean" },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Button",
    variant: "default",
    size: "default",
  },
};

export const Destructive: Story = {
  args: {
    children: "Delete",
    variant: "destructive",
  },
};

export const Outline: Story = {
  args: {
    children: "Outline",
    variant: "outline",
  },
};

export const Secondary: Story = {
  args: {
    children: "Secondary",
    variant: "secondary",
  },
};

export const Ghost: Story = {
  args: {
    children: "Ghost",
    variant: "ghost",
  },
};

export const Link: Story = {
  args: {
    children: "Link Button",
    variant: "link",
  },
};

export const Small: Story = {
  args: {
    children: "Small",
    size: "sm",
  },
};

export const Large: Story = {
  args: {
    children: "Large",
    size: "lg",
  },
};

export const ExtraSmall: Story = {
  args: {
    children: "XS",
    size: "xs",
  },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <Download /> Download
      </>
    ),
  },
};

export const IconOnly: Story = {
  args: {
    children: <Zap />,
    size: "icon",
  },
};

export const Disabled: Story = {
  args: {
    children: "Disabled",
    disabled: true,
  },
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <div className="flex flex-col gap-4 items-start">
      <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-[18px] py-2 gap-1.5">
        <Zap className="w-4 h-4" />
        <span className="text-sm font-medium">发布新内容</span>
      </Button>
      <Button className="bg-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]/80 rounded-lg py-2.5">
        <span className="text-[13px] font-medium">立即发布</span>
      </Button>
      <Button
        variant="outline"
        className="bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)] rounded-full gap-1.5 py-2"
      >
        <ArrowRight className="w-3.5 h-3.5" />
        <span className="text-[13px] font-medium">查看更多</span>
      </Button>
      <Button variant="destructive">
        <Trash2 className="w-4 h-4" />
        Delete Item
      </Button>
    </div>
  ),
};

export const AllVariants: Story = {
  name: "All Variants",
  render: () => (
    <div className="flex flex-wrap gap-3">
      <Button variant="default">Default</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
};

export const AllSizes: Story = {
  name: "All Sizes",
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Button size="xs">Extra Small</Button>
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
      <Button size="icon"><Zap /></Button>
      <Button size="icon-xs"><Zap /></Button>
      <Button size="icon-sm"><Zap /></Button>
      <Button size="icon-lg"><Zap /></Button>
    </div>
  ),
};
