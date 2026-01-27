import type { Meta, StoryObj } from "@storybook/react";
import { User } from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const meta = {
  title: "UI/Card",
  component: Card,
  tags: ["autodocs"],
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description goes here.</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm">Card content area.</p>
      </CardContent>
      <CardFooter>
        <Button>Action</Button>
      </CardFooter>
    </Card>
  ),
};

export const WithAction: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Project Settings</CardTitle>
        <CardDescription>Manage your project configuration.</CardDescription>
        <CardAction>
          <Button variant="outline" size="sm">Edit</Button>
        </CardAction>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">Your project is currently active.</p>
      </CardContent>
    </Card>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <div className="flex flex-col gap-4">
      {/* Image Card */}
      <Card className="w-[300px] bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
        <div
          className="w-full h-[180px] bg-cover bg-center bg-[var(--nf-dark-bg)]"
        />
        <div className="p-3 flex flex-col gap-1.5">
          <p className="text-[13px] font-medium text-[var(--nf-white)]">
            创新设计大赛 第七届
          </p>
          <div className="flex items-center gap-1.5">
            <div className="w-[18px] h-[18px] rounded-full bg-[#555555]" />
            <span className="text-[11px] text-[var(--nf-muted)]">JioNan</span>
          </div>
        </div>
      </Card>

      {/* Proposal Card */}
      <Card className="w-[400px] bg-[var(--nf-card-bg)] border-none rounded-[12px] p-3 flex flex-row gap-3">
        <div className="w-[100px] h-[100px] rounded-lg bg-[var(--nf-dark-bg)] shrink-0" />
        <div className="flex flex-col gap-1.5 min-w-0">
          <p className="text-[13px] font-medium text-[var(--nf-white)] line-clamp-2">
            全文智算 海天仿仿AI服装设计
          </p>
          <p className="text-[12px] text-[var(--nf-muted)] line-clamp-2">
            "全文智算"搭配虚拟时尚技术，让AI帮你建立定制化标签式造型。
          </p>
          <div className="flex items-center gap-2 mt-auto">
            <div className="w-5 h-5 rounded-full bg-[var(--nf-lime)] flex items-center justify-center">
              <User className="w-2.5 h-2.5 text-[var(--nf-surface)]" />
            </div>
            <span className="text-[11px] text-[var(--nf-muted)]">Jacksen</span>
          </div>
        </div>
      </Card>
    </div>
  ),
};

export const PromoCard: Story = {
  name: "Promo Banner Card",
  render: () => (
    <div className="bg-[var(--nf-lime)] rounded-[16px] p-5 flex flex-col gap-2 w-[280px]">
      <span className="font-heading text-[22px] font-bold text-[var(--nf-surface)]">
        来协创,创个业
      </span>
      <span className="text-[12px] text-[var(--nf-dark-bg)]">
        来来看看Synnovator特特色。
      </span>
    </div>
  ),
};
