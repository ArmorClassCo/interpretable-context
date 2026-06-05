import { PrismaClient } from "@prisma/client";

// Postgres via Prisma.
export const db = new PrismaClient();
