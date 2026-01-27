import type { Meta, StoryObj } from "@storybook/react";
import { Separator } from "@/components/ui/separator";

const meta = {
  title: "UI/Separator",
  component: Separator,
  tags: ["autodocs"],
  argTypes: {
    orientation: {
      control: "select",
      options: ["horizontal", "vertical"],
    },
    decorative: { control: "boolean" },
  },
} satisfies Meta<typeof Separator>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Horizontal: Story = {
  render: () => (
    <div className="w-[300px]">
      <div className="space-y-1">
        <h4 className="text-sm font-medium leading-none">Radix Primitives</h4>
        <p className="text-sm text-muted-foreground">
          An open-source UI component library.
        </p>
      </div>
      <Separator className="my-4" />
      <div className="flex h-5 items-center space-x-4 text-sm">
        <div>Blog</div>
        <Separator orientation="vertical" />
        <div>Docs</div>
        <Separator orientation="vertical" />
        <div>Source</div>
      </div>
    </div>
  ),
};

export const Vertical: Story = {
  render: () => (
    <div className="flex h-5 items-center space-x-4 text-sm">
      <div>Blog</div>
      <Separator orientation="vertical" />
      <div>Docs</div>
      <Separator orientation="vertical" />
      <div>Source</div>
    </div>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <div className="w-[300px] flex flex-col gap-3">
      <span className="text-[var(--nf-white)] text-sm font-medium">Section A</span>
      <Separator className="bg-[var(--nf-dark-bg)]" />
      <span className="text-[var(--nf-white)] text-sm font-medium">Section B</span>
      <Separator className="bg-[var(--nf-dark-bg)]" />
      <span className="text-[var(--nf-white)] text-sm font-medium">Section C</span>
    </div>
  ),
};
