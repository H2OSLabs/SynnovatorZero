import type { Meta, StoryObj } from "@storybook/react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

const meta = {
  title: "UI/ScrollArea",
  component: ScrollArea,
  tags: ["autodocs"],
} satisfies Meta<typeof ScrollArea>;

export default meta;
type Story = StoryObj<typeof meta>;

const tags = Array.from({ length: 50 }, (_, i) => `Item ${i + 1}`);

export const Vertical: Story = {
  render: () => (
    <ScrollArea className="h-72 w-48 rounded-md border">
      <div className="p-4">
        <h4 className="mb-4 text-sm font-medium leading-none">Tags</h4>
        {tags.map((tag) => (
          <div key={tag}>
            <div className="text-sm">{tag}</div>
            <Separator className="my-2" />
          </div>
        ))}
      </div>
    </ScrollArea>
  ),
};

export const Horizontal: Story = {
  render: () => (
    <ScrollArea className="w-96 whitespace-nowrap rounded-md border">
      <div className="flex w-max space-x-4 p-4">
        {Array.from({ length: 20 }, (_, i) => (
          <div
            key={i}
            className="w-[150px] h-[100px] rounded-md bg-muted flex items-center justify-center shrink-0"
          >
            <span className="text-sm text-muted-foreground">Card {i + 1}</span>
          </div>
        ))}
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <ScrollArea className="h-72 w-64 rounded-[12px] bg-[var(--nf-card-bg)] border-none">
      <div className="p-4 flex flex-col gap-2">
        <h4 className="text-sm font-semibold text-[var(--nf-white)]">提案列表</h4>
        {Array.from({ length: 20 }, (_, i) => (
          <div
            key={i}
            className="flex items-center gap-2 p-2 rounded-lg hover:bg-[var(--nf-dark-bg)] cursor-pointer"
          >
            <div className="w-8 h-8 rounded-full bg-[var(--nf-lime)] shrink-0 flex items-center justify-center">
              <span className="text-xs font-bold text-[var(--nf-surface)]">{i + 1}</span>
            </div>
            <span className="text-[13px] text-[var(--nf-light-gray)]">提案 #{i + 1}</span>
          </div>
        ))}
      </div>
    </ScrollArea>
  ),
};
