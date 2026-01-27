import type { Meta, StoryObj } from "@storybook/react";
import { User, Check } from "lucide-react";
import {
  Avatar,
  AvatarImage,
  AvatarFallback,
  AvatarBadge,
  AvatarGroup,
  AvatarGroupCount,
} from "@/components/ui/avatar";

const meta = {
  title: "UI/Avatar",
  component: Avatar,
  tags: ["autodocs"],
  argTypes: {
    size: {
      control: "select",
      options: ["default", "sm", "lg"],
    },
  },
} satisfies Meta<typeof Avatar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Avatar>
      <AvatarFallback>CN</AvatarFallback>
    </Avatar>
  ),
};

export const WithImage: Story = {
  render: () => (
    <Avatar>
      <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
      <AvatarFallback>CN</AvatarFallback>
    </Avatar>
  ),
};

export const Small: Story = {
  render: () => (
    <Avatar size="sm">
      <AvatarFallback>S</AvatarFallback>
    </Avatar>
  ),
};

export const Large: Story = {
  render: () => (
    <Avatar size="lg">
      <AvatarFallback>LG</AvatarFallback>
    </Avatar>
  ),
};

export const WithBadge: Story = {
  render: () => (
    <Avatar size="lg">
      <AvatarFallback>AB</AvatarFallback>
      <AvatarBadge>
        <Check />
      </AvatarBadge>
    </Avatar>
  ),
};

export const Group: Story = {
  render: () => (
    <AvatarGroup>
      <Avatar>
        <AvatarFallback>A</AvatarFallback>
      </Avatar>
      <Avatar>
        <AvatarFallback>B</AvatarFallback>
      </Avatar>
      <Avatar>
        <AvatarFallback>C</AvatarFallback>
      </Avatar>
      <AvatarGroupCount>+5</AvatarGroupCount>
    </AvatarGroup>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <div className="flex items-center gap-4">
      <Avatar className="bg-[var(--nf-blue)]">
        <AvatarFallback className="bg-[var(--nf-blue)]">
          <User className="w-4 h-4 text-[var(--nf-white)]" />
        </AvatarFallback>
      </Avatar>
      <Avatar className="bg-[var(--nf-lime)]">
        <AvatarFallback className="bg-[var(--nf-lime)]">
          <User className="w-4 h-4 text-[var(--nf-surface)]" />
        </AvatarFallback>
      </Avatar>
      <Avatar className="bg-[var(--nf-pink)]">
        <AvatarFallback className="bg-[var(--nf-pink)]">
          <User className="w-4 h-4 text-[var(--nf-surface)]" />
        </AvatarFallback>
      </Avatar>
      <Avatar className="bg-[var(--nf-cyan)]">
        <AvatarFallback className="bg-[var(--nf-cyan)]">
          <User className="w-4 h-4 text-[var(--nf-surface)]" />
        </AvatarFallback>
      </Avatar>
    </div>
  ),
};

export const AllSizes: Story = {
  name: "All Sizes",
  render: () => (
    <div className="flex items-center gap-4">
      <Avatar size="sm">
        <AvatarFallback>SM</AvatarFallback>
      </Avatar>
      <Avatar size="default">
        <AvatarFallback>MD</AvatarFallback>
      </Avatar>
      <Avatar size="lg">
        <AvatarFallback>LG</AvatarFallback>
      </Avatar>
    </div>
  ),
};
